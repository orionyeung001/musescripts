#include "test_abc.h"

void process(TH1F* h_qdc)
{
	Int_t n_events = 100000;
	// Int_t n_events = (Int_t)mc_tree->GetEntries();

	for ( Int_t i = 0; i < n_events; i++ )
	{
		mc_tree->GetEntry(i);
		if ( 0 == fmod(i,100000) )
			printf( " .. processed %d events\n", i);

		bool bar_is_hit = false;
		for (int j = 0; j < mcdata->CAL_Hit; j++)
		{
			int copyID = (*mcdata->CAL_CopyID)[j];
			if ( copyID == bar )
			{
				bar_is_hit = true;
				double event_pedestal = gRandom->Gaus(calib_pedestal, calib_pedestal_sigma);
				double e = (*mcdata->CAL_PhotonY)[j] / calib_ecalib;
				double calib_lightoutput_rel_sigma = a / TMath::Sqrt(e*0.001) + b + c / (e*0.001);
				double ph = std::fmin(gRandom->Gaus(e, e * calib_lightoutput_rel_sigma) + event_pedestal, 3840); // QDC channels
				h_qdc->Fill(ph);
			}
		}

		if ( !bar_is_hit )
		{
			double event_pedestal = gRandom->Gaus(calib_pedestal, calib_pedestal_sigma);
			h_qdc->Fill(event_pedestal);
		}
	}

	return;
}

void test_abc()
{
	/// setup

	TFile *run_file = new TFile(Form("~/muse/root_files/run%d_PBG_Detail.root",run));
	TH1F* h_data = (TH1F*)run_file->Get(Form("Individual Bars/x = %d, y = %d/QDC e Hits", bar_x, bar_y));
	h_data->Rebin(10);
	scale_to = interate_signal(h_data);

	TFile *g4_file = new TFile(Form("~/muse_geant4/g4psi_%d.root",run));
	mc_tree = (TTree*)g4_file->Get("T");
	if ( mc_tree == NULL )
	{
		printf("Cannot find tree!\n");
		return;
	}
	else
		printf("\n Found tree ...\n\n");

	mcdata = new mcdataCAL(mc_tree, "CAL_PbG");
	bool has_mc_data = mcdata->is_available();
	if (has_mc_data)
		printf(" Found data ... trying to process ...\n");

	init_params();

	/// process - first loop

	TH1F* h_qdc = new TH1F("h_qdc",";QDC (ch.);Counts",4500/10,0,4500);

	process(h_qdc);
	h_qdc->Scale(scale_to/interate_signal(h_qdc));
	double parity = find_parity(h_qdc, h_data);
	printf(" a initial: %f, parity: %f\n", a, parity);

	TH1F* h_clone = (TH1F*)h_qdc->Clone();

	/// process - test parameters

	double d_parity = 100;
	double d_parity_new = 100;

	int loop_count = 1;
	a = param_a.min + param_a.step;

	// while ( abs(d_parity_new) <= abs(d_parity) && a < param_a.max )
	while ( a < param_a.max )
	{
		printf(" iteration %d\n", loop_count);
		d_parity = d_parity_new;

		h_qdc->Reset();
		process(h_qdc);
		h_qdc->Scale(scale_to/interate_signal(h_qdc));

		double parity_new = find_parity(h_qdc, h_data);
		d_parity_new = abs(parity_new) - abs(parity);
		printf(" a: %f, parity_new: %f, d_parity_new: %f, d_parity: %f\n", a, parity_new, d_parity_new, d_parity);

		if ( abs(d_parity_new) <= abs(d_parity) )
		{
			parity = parity_new;
			param_a.value = a;
		}

		a += param_a.step;
		loop_count ++;
		printf(" next a: %f\n", a);

		if ( ! (abs(d_parity_new) <= abs(d_parity)) )
			printf(" d_parity_new > d_parity, quitting loop ...\n" );
		if ( ! (a < param_a.max) )
			printf(" a > param_a.max, quitting loop ...\n" );

	}

	printf("\n a final: %f, parity: %f\n", param_a.value, parity);


	/// plot result

	TCanvas *c = new TCanvas("c","",600,600);
	gPad->SetLogy();

	h_data->Draw("HIST SAME");
	h_data->SetLineColor(kRed);
	h_clone->Draw("HIST SAME");
	h_clone->SetLineColor(kOrange+2);
	h_qdc->Draw("HIST SAME");
	h_data->GetXaxis()->SetRangeUser(0,1200);
	h_qdc->GetXaxis()->SetRangeUser(0,1200);

	printf("\n Finished!\n\n");

	return;
}
