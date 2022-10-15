#pragma once
#include "../Artel.h"


class Image
{
public:
	Image(ID3D11Device* m_pd3dDevice, ID3D11DeviceContext* m_pd3dDeviceContext, IDXGISwapChain* m_pSwapChain, ID3D11RenderTargetView* m_mainRenderTargetView);
	bool LoadTextureFromFile(const char* filename, ID3D11ShaderResourceView** out_srv, int* out_width, int* out_height);
private:
	ID3D11Device* g_pd3dDevice;
	ID3D11DeviceContext* g_pd3dDeviceContext;
	IDXGISwapChain* g_pSwapChain;
	ID3D11RenderTargetView* g_mainRenderTargetView;

};

