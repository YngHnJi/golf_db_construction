
// kinect_guiDlg.h: 헤더 파일
//

#pragma once

#include <k4a/k4a.hpp>
#include <k4a/k4a.h>
#include <k4arecord/record.h>
#include <k4arecord/record.hpp>

#include <iostream>
#include <cstdio>
#include <vector>
#include <array>
#include <conio.h>
#include <direct.h>

#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "init_device.hpp"

#include "Pixel.h"
#include "DepthPixelColorizer.h"
#include "StaticImageProperties.h"

using namespace std;
using namespace cv;
using namespace sen;

// CkinectguiDlg 대화 상자
class CkinectguiDlg : public CDialogEx
{
// 생성입니다.
public:
	CkinectguiDlg(CWnd* pParent = nullptr);	// 표준 생성자입니다.

// 대화 상자 데이터입니다.
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_KINECT_GUI_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 지원입니다.


// 구현입니다.
protected:
	HICON m_hIcon;

	// 생성된 메시지 맵 함수
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CStatic m_picture;
	//cv::VideoCapture* capture;
	cv::Mat mat_frame;
	CImage cimage_mfc;
	int m_record_flag;
	afx_msg void OnTimer(UINT_PTR nIDEvent);
	afx_msg void OnDestroy();
	afx_msg void OnClickedButtonRecord();
	afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
	RECT r;
	cv::Size winSize;
	
	//for kinect azure
	k4a_device_configuration_t config;
	k4a::device device;

	k4a::capture capture;
	k4a::record recording;
};
