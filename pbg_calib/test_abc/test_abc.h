#include "mcdataCAL.cpp"
#include "mcdata.cpp"

const int run = 13057;
const int p_run = 110; // MeV/c
const int bar_x = 4;
const int bar_y = 4;
const int bar = 27;

const double calib_pedestal = 128.80;
const double calib_pedestal_sigma = 3.275;

double calib_ecalib = 2.4;
double a = 0.00; // statistic
double b = 0.05; // calibration
double c = 0.001; // noise

double sig_range[2] = {400, 2000};

TTree *mc_tree;
mcdataCAL *mcdata;

// TH1F* h_qdc;
// TH1F* h_data;

double scale_to = 1.;

struct param{
	double value;
	double min;
	double max;
	double step;
};

param param_a;
param param_b;
param param_c;
param param_e;

void init_params()
{
	param_a.value = 0.0;
	param_a.min = 0.00;
	param_a.max = 0.10;
	param_a.step = 0.01;

	param_b.value = 0.0;
	param_b.min = 0.00;
	param_b.max = 0.1;
	param_b.step = 0.04;

	param_c.value = 0.0;
	param_c.min = 0.00;
	param_c.max = 0.03;
	param_c.step = 0.01;

	param_e.value = 0.0;
	param_e.min = 1.0;
	param_e.max = 3.0;
	param_e.step = 0.5;

	return;
}

double find_parity(TH1F* h_qdc, TH1F* h_data)
{
	double parity = 0;
	int min_bin = h_qdc->FindBin(sig_range[0]);
	int max_bin = h_qdc->FindBin(sig_range[1]);
	for (int i = min_bin; i < max_bin; i ++ )
		parity = abs(h_qdc->GetBinContent(i)-h_data->GetBinContent(i)) + parity;

	return parity;
}

double interate_signal(TH1F* h)
{
	double integral = 0;
	int min_bin = h->FindBin(sig_range[0]);
	int max_bin = h->FindBin(sig_range[1]);
	for (int i = min_bin; i < max_bin; i ++ )
		integral += h->GetBinContent(i);

	// printf("min_bin = %d, integral = %f\n", min_bin, integral);

	return integral;
}
