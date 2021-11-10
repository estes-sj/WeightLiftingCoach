/*
 * Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

#include "detectNet.h"
#include "cudaUtility.h"
#include "cudaAlphaBlend.cuh"
#include <cstdlib>
#include <cmath>

#define MIN(a,b)	(a < b ? a : b)
#define MAX(a,b)	(a > b ? a : b)

template<typename T> inline __device__ __host__ T sqr(T x) 				    { return x*x; }

inline __device__ __host__ float dist2(float x0, float y0, float x1, float y1) { return sqr(x0-x1) + sqr(y0-y1); }
inline __device__ __host__ float dist(float x0, float y0, float x1, float y1)  { return sqrtf(dist2(x0,y0,x1,y1)); }



template<typename T>
__global__ void gpuDetectionOverlay( T* input, T* output, int width, int height, detectNet::Detection* detections, int numDetections, float4* colors ) 
{
	const int x = blockIdx.x * blockDim.x + threadIdx.x;
	const int y = blockIdx.y * blockDim.y + threadIdx.y;

	if( x >= width || y >= height )
		return;

	const int px_idx = y * width + x;
	T px = input[px_idx];
	
	const float fx = x;
	const float fy = y;
	
	for( int n=0; n < numDetections; n++ )
	{
		const detectNet::Detection det = detections[n];

		// check if this pixel is inside the bounding box
		if( fx >= det.Left && fx <= det.Right && fy >= det.Top && fy <= det.Bottom )
		{
			const float4 color = colors[det.ClassID];	

			const float alpha = color.w / 255.0f;
			const float ialph = 1.0f - alpha;

			px.x = alpha * color.x + ialph * px.x;
			px.y = alpha * color.y + ialph * px.y;
			px.z = alpha * color.z + ialph * px.z;
		}
	}
	
	output[px_idx] = px;	 
}

// Old Overlay
// template<typename T>
// __global__ void gpuDetectionOverlayBox( T* input, T* output, int imgWidth, int imgHeight, int x0, int y0, int boxWidth, int boxHeight, const float4 color ) 
// {
// 	const int box_x = blockIdx.x * blockDim.x + threadIdx.x;
// 	const int box_y = blockIdx.y * blockDim.y + threadIdx.y;

// 	if( box_x >= imgWidth || box_y >= imgHeight )
// 		return;

// 	const int x = box_x + x0;
// 	const int y = box_y + y0;

// 	if( x >= imgWidth || y >= imgHeight )
// 	return;

// 	T px = input[ y * imgWidth + x ];

// 	const float alpha = color.w / 255.0f;
// 	const float ialph = 1.0f - alpha;

// 	px.x = alpha * color.x + ialph * px.x;
// 	px.y = alpha * color.y + ialph * px.y;
// 	px.z = alpha * color.z + ialph * px.z;

// 	output[y * imgWidth + x] = px;
// }

// Line Distance Squard
inline __device__ float lineDistanceSquared(float x, float y, float x0, float y0, float x1, float y1)
{
	const float d = dist2(x0, y0, x1, y1);
	const float t = ( (x-x0) * (x1-x0) + (y-y0) * (y1-y0) ) / d;
	const float u = MAX( 0, MIN(1, t) );
	
	return dist2(x, y, x0 + u * (x1 - x0), y0 + u * (y1 - y0));
}

// New Overlay
template<typename T>
__global__ void gpuDrawLine( T* img, int imgWidth, int imgHeight, int offset_x, int offset_y, int x0, int y0, int x1, int y1, const float4 color, float line_width2 ) 
{
	const int x = blockIdx.x * blockDim.x + threadIdx.x + offset_x;
	const int y = blockIdx.y * blockDim.y + threadIdx.x + offset_y;

	if( x >= imgWidth || y >= imgHeight )
		return;

	if( lineDistanceSquared(x, y, x0, y0, x1, y1) <= line_width2 )
	{
		const int idx = y * imgWidth + x;
		img[idx] = cudaAlphaBlend(img[idx], color );
	}

}

// // New cudaDrawLine 
// cudaError_t cudaDrawLine( void* input, void* output, size_t width, size_t height, imageFormat format, int x1, int y1, int x2, int y2, const float4& color, float line_width )
// {
// 	if( !input || !output || width == 0 || height == 0 || line_width <= 0 )
// 		return cudaErrorInvalidValue;
	
// 	// check for lines < 2 pixels in length
// 	if( dist(x1,y1,x2,y2) < 2.0 )
// 	{
// 		return cudaSuccess;
// 	}
// 	// if the input and output images are different, copy the input to the output
// 	// this is because we only launch the kernel in the approximate area of the circle
// 	if( input != output )
// 		CUDA(cudaMemcpy(output, input, imageFormatSize(format, width, height), cudaMemcpyDeviceToDevice));
	

// 	// find a box around the line
// 	const int left = MIN(x1,x2) - line_width;
// 	const int right = MAX(x1,x2) + line_width;
// 	const int top = MIN(y1,y2) - line_width;
// 	const int bottom = MAX(y1,y2) + line_width;

// 	// launch kernel
// 	const dim3 blockDim(8, 8);
// 	const dim3 gridDim(iDivUp(right - left, blockDim.x), iDivUp(bottom - top, blockDim.y));

// 	#define LAUNCH_DRAW_LINE(type) \
// 		gpuDrawLine<type><<<gridDim, blockDim>>>((type*)output, width, height, left, top, x1, y1, x2, y2, color, line_width * line_width)
	
// 	if( format == IMAGE_RGB8 )
// 		LAUNCH_DRAW_LINE(uchar3);
// 	else if( format == IMAGE_RGBA8 )
// 		LAUNCH_DRAW_LINE(uchar4);
// 	else if( format == IMAGE_RGB32F )
// 		LAUNCH_DRAW_LINE(float3); 
// 	else if( format == IMAGE_RGBA32F )
// 		LAUNCH_DRAW_LINE(float4);
// 	else
// 	{
// 		return cudaErrorInvalidValue;
// 	}
		
// 	return cudaGetLastError();
// }

// Old Launch Overlay
// template<typename T>
// cudaError_t launchDetectionOverlay( T* input, T* output, uint32_t width, uint32_t height, detectNet::Detection* detections, int numDetections, float4* colors )
// {
// 	if( !input || !output || width == 0 || height == 0 || !detections || numDetections == 0 || !colors )
// 		return cudaErrorInvalidValue;
			
// 	// this assumes that the output already has the input image copied to it,
// 	// which if input != output, is done first by detectNet::Detect()
// 	for( int n=0; n < numDetections; n++ )
// 	{
// 		const int boxWidth = (int)detections[n].Width();
// 		const int boxHeight = (int)detections[n].Height();

// 		// launch kernel
// 		const dim3 blockDim(8, 8);
// 		const dim3 gridDim(iDivUp(boxWidth,blockDim.x), iDivUp(boxHeight,blockDim.y));

// 		gpuDetectionOverlayBox<T><<<gridDim, blockDim>>>(input, output, width, height, (int)detections[n].Left, (int)detections[n].Top, boxWidth, boxHeight, colors[detections[n].ClassID]); 
// 	}

// 	return cudaGetLastError();
// }

// New Launch Detection
// template<typename T>
// cudaError_t launchDetectionOverlay( T* input, T* output, uint32_t width, uint32_t height, int x0, int y0, int x1, int y1, const float4 color, const float line_width )
// {
// 	if( !input || !output || width == 0 || height == 0 )
// 		return cudaErrorInvalidValue;

// 		// find a box around the line
// 		const int left = MIN(x0,x1) - line_width;
// 		const int right = MAX(x0,x1) + line_width;
// 		const int top = MIN(y0,y1) - line_width;
// 		const int bottom = MAX(y0,y1) + line_width;
	
// 		// launch kernel
// 		const dim3 blockDim(8, 8);
// 		const dim3 gridDim(iDivUp( right - left, blockDim.x ), iDivUp( bottom - top, blockDim.y ) );

// 		gpuDrawLine<T><<<gridDim, blockDim>>>(output, width, height, left, top, x0, y0, x1, y1, color, line_width * line_width);
// 		cudaDeviceSynchronize();

// 	return cudaGetLastError();
// }

// cudaError_t cudaDetectionOverlay( void* input, void* output, uint32_t width, uint32_t height, imageFormat format, int x0, int y0, int x1, int y1, const float4& color, const float line_width )
// {
// 	if( format == IMAGE_RGB8 )
// 		return launchDetectionOverlay<uchar3>((uchar3*)input, (uchar3*)output, width, height, x0, y0, x1, y1, color, line_width); 
// 	else if( format == IMAGE_RGBA8 )
// 		return launchDetectionOverlay<uchar4>((uchar4*)input, (uchar4*)output, width, height, x0, y0, x1, y1, color, line_width);  
// 	else if( format == IMAGE_RGB32F )
// 		return launchDetectionOverlay<float3>((float3*)input, (float3*)output, width, height, x0, y0, x1, y1, color, line_width);  
// 	else if( format == IMAGE_RGBA32F )
// 		return launchDetectionOverlay<float4>((float4*)input, (float4*)output, width, height, x0, y0, x1, y1, color, line_width); 
// 	else
// 		return cudaErrorInvalidValue;
// }

