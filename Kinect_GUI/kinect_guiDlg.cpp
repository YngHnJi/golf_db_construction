
// kinect_guiDlg.cpp: 구현 파일
//

#include "pch.h"
#include "framework.h"
#include "kinect_gui.h"
#include "kinect_guiDlg.h"
#include "afxdialogex.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


struct kinect_img_container {
	std::vector<Pixel> depthTextureBuffer;
	std::vector<Pixel> irTextureBuffer;
	uint8_t* colorTextureBuffer;

	k4a::image colorImage;
	k4a::image depthImage;
	k4a::image irImage;

	cv::Mat colorFrame;
	cv::Mat depthFrame;
	cv::Mat irFrame;

	cv::Mat colorFrame_converted;
};


// 응용 프로그램 정보에 사용되는 CAboutDlg 대화 상자입니다.

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 대화 상자 데이터입니다.
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 지원입니다.

// 구현입니다.
protected:
	DECLARE_MESSAGE_MAP()
public:
//	afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
//	ON_WM_KEYDOWN()
END_MESSAGE_MAP()


// CkinectguiDlg 대화 상자



CkinectguiDlg::CkinectguiDlg(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_KINECT_GUI_DIALOG, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
	m_record_flag = 0;
}

void CkinectguiDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_PICTURE, m_picture);
}

BEGIN_MESSAGE_MAP(CkinectguiDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_WM_TIMER()
	ON_WM_DESTROY()
	ON_BN_CLICKED(IDC_BUTTON_RECORD, &CkinectguiDlg::OnClickedButtonRecord)
	ON_WM_KEYDOWN()
END_MESSAGE_MAP()


// CkinectguiDlg 메시지 처리기

BOOL CkinectguiDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 시스템 메뉴에 "정보..." 메뉴 항목을 추가합니다.

	// IDM_ABOUTBOX는 시스템 명령 범위에 있어야 합니다.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != nullptr)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 이 대화 상자의 아이콘을 설정합니다.  응용 프로그램의 주 창이 대화 상자가 아닐 경우에는
	//  프레임워크가 이 작업을 자동으로 수행합니다.
	SetIcon(m_hIcon, TRUE);			// 큰 아이콘을 설정합니다.
	SetIcon(m_hIcon, FALSE);		// 작은 아이콘을 설정합니다.

	// TODO: 여기에 추가 초기화 작업을 추가합니다.
	//// Kinect Azure Init here
	cv::setBreakOnError(true);

	const uint32_t deviceCount = k4a::device::get_installed_count();
	if (deviceCount == 0)
	{
		cout << "no azure kinect devices detected!" << endl;
	}
	m_record_flag = 0; // record button control

	m_picture.GetClientRect(&r);
	winSize = cv::Size(r.right, r.bottom);

	cout << "Configuring Kinect Device Started" << endl;
	init_kinect(device, config);
	cout << "Configuring Kinect Device Done" << endl;


	SetTimer(1000, 1, NULL);

	return TRUE;  // 포커스를 컨트롤에 설정하지 않으면 TRUE를 반환합니다.
}

void CkinectguiDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 대화 상자에 최소화 단추를 추가할 경우 아이콘을 그리려면
//  아래 코드가 필요합니다.  문서/뷰 모델을 사용하는 MFC 애플리케이션의 경우에는
//  프레임워크에서 이 작업을 자동으로 수행합니다.

void CkinectguiDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 그리기를 위한 디바이스 컨텍스트입니다.

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 클라이언트 사각형에서 아이콘을 가운데에 맞춥니다.
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 아이콘을 그립니다.
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

// 사용자가 최소화된 창을 끄는 동안에 커서가 표시되도록 시스템에서
//  이 함수를 호출합니다.
HCURSOR CkinectguiDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void CkinectguiDlg::OnTimer(UINT_PTR nIDEvent)
{
	kinect_img_container im_container;


	if (device.get_capture(&capture, std::chrono::milliseconds(0)))
	{
		if ((m_record_flag == 1) && (recording.is_valid() == true)) {
			recording.write_capture(capture);
		}

		//get image from capture
		im_container.colorImage = capture.get_color_image();
		//im_container.depthImage = capture.get_depth_image();
		//im_container.irImage = capture.get_ir_image();

		im_container.colorTextureBuffer = im_container.colorImage.get_buffer();
		//ColorizeDepthImage(im_container.depthImage, DepthPixelColorizer::ColorizeBlueToRed, GetDepthModeRange(config.depth_mode), &im_container.depthTextureBuffer);
		//ColorizeDepthImage(im_container.irImage, DepthPixelColorizer::ColorizeGreyscale, GetIrLevels(K4A_DEPTH_MODE_PASSIVE_IR), &im_container.irTextureBuffer);

		//convert image to cv::Mat format 
		im_container.colorFrame = cv::Mat(im_container.colorImage.get_height_pixels(), im_container.colorImage.get_width_pixels(), CV_8UC2, im_container.colorTextureBuffer); // YUY2 format to show
		//im_container.depthFrame = cv::Mat(im_container.depthImage.get_height_pixels(), im_container.depthImage.get_width_pixels(), CV_8UC4, im_container.depthTextureBuffer.data());
		//im_container.irFrame = cv::Mat(im_container.irImage.get_height_pixels(), im_container.irImage.get_width_pixels(), CV_8UC4, im_container.irTextureBuffer.data());

		cvtColor(im_container.colorFrame, im_container.colorFrame, COLOR_YUV2BGR_YUY2); //COLOR_YUV2BGR_YUY2, COLOR_YUV2BGR_UYVY
		//cv::imshow("kinect color frame master", im_container.colorFrame);
		//cv::imshow("kinect depth map master", im_container.depthFrame);
		//cv::imshow("kinect ir frame master", im_container.irFrame);

		//cv::Mat to BitMap to show image on Picture Control
		int bpp = 8 * im_container.colorFrame.elemSize();
		assert((bpp == 8 || bpp == 24 || bpp == 32));

		int padding = 0;
		//32 bit image is always DWORD aligned because each pixel requires 4 bytes
		if (bpp < 32)
			padding = 4 - (im_container.colorFrame.cols % 4);

		if (padding == 4)
			padding = 0;

		int border = 0;
		//32 bit image is always DWORD aligned because each pixel requires 4 bytes
		if (bpp < 32)
		{
			border = 4 - (im_container.colorFrame.cols % 4);
		}

		cimage_mfc.Create(winSize.width, winSize.height, 24);

		cv::resize(im_container.colorFrame, im_container.colorFrame, cv::Size(winSize.width, winSize.height));

		BITMAPINFO* bitInfo = (BITMAPINFO*)malloc(sizeof(BITMAPINFO) + 256 * sizeof(RGBQUAD));
		bitInfo->bmiHeader.biBitCount = bpp;
		bitInfo->bmiHeader.biWidth = im_container.colorFrame.cols;
		bitInfo->bmiHeader.biHeight = -im_container.colorFrame.rows;
		bitInfo->bmiHeader.biPlanes = 1;
		bitInfo->bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
		bitInfo->bmiHeader.biCompression = BI_RGB;
		bitInfo->bmiHeader.biClrImportant = 0;
		bitInfo->bmiHeader.biClrUsed = 0;
		bitInfo->bmiHeader.biSizeImage = 0;
		bitInfo->bmiHeader.biXPelsPerMeter = 0;
		bitInfo->bmiHeader.biYPelsPerMeter = 0;

		SetDIBitsToDevice(cimage_mfc.GetDC(),
			//destination rectangle
			0, 0, winSize.width, winSize.height,
			0, 0, 0, im_container.colorFrame.rows,
			im_container.colorFrame.data, bitInfo, DIB_RGB_COLORS);

		HDC dc = ::GetDC(m_picture.m_hWnd); //get image handler to 'dc'
		cimage_mfc.BitBlt(dc, 0, 0); // image handle, nXDest, nYDest

		::ReleaseDC(m_picture.m_hWnd, dc);

		cimage_mfc.ReleaseDC();
		cimage_mfc.Destroy();

	}
	CDialogEx::OnTimer(nIDEvent);
}


void CkinectguiDlg::OnDestroy()
{
	CDialogEx::OnDestroy();

	// TODO: 여기에 메시지 처리기 코드를 추가합니다.
}


void CkinectguiDlg::OnClickedButtonRecord()
{
	// TODO: 여기에 컨트롤 알림 처리기 코드를 추가합니다.
	
	if (m_record_flag == 0)
	{
		AfxMessageBox(_T("Record Start"));
		m_record_flag = 1;
		string filename = "output\\check.mkv";
		init_record(device, config, recording, filename); // init recorder
	}
	else // save file
	{
		AfxMessageBox(_T("Saving Record"));
		
		recording.close();
		recording.flush();
	}

}


void CkinectguiDlg::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags)
{
	// TODO: 여기에 메시지 처리기 코드를 추가 및/또는 기본값을 호출합니다.
	AfxMessageBox(_T("Button Pushed"));


	CDialogEx::OnKeyDown(nChar, nRepCnt, nFlags);
}
