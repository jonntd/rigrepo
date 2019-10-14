//Maya ASCII 2018ff09 scene
//Name: biped_picker.ma
//Last modified: Mon, Oct 14, 2019 06:43:08 AM
//Codeset: 1252
requires maya "2018ff09";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811122215-49253d42f6";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "brow_all_l__button";
	rename -uid "C9DA8105-4958-5589-D19E-D388373463F9";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr -k on ".selectableItems" -type "string" "['brow_inner_l', 'brow_main_l', 'brow_peak_l']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_all_l__buttonShape" -p "brow_all_l__button";
	rename -uid "057C517B-4DA9-510A-BA35-2DA76C0FA183";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.32542479038238525 0.61581796407699585 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 6 ".uvst[0].uvsp[0:5]" -type "float2" 0.084756069 4.139903e-17
		 0.27120072 0 0.32542479 0.61581796 0.081356212 1 0 0.93220317 0.19435091 0.62485754;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 6 ".clst[0].clsp[0:5]"  0 0.61870003 1 1 0 0.61870003 1
		 1 0 0.61870003 1 1 0 0.61870003 1 1 0 0.61870003 1 1 0 0.61870003 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 6 ".pt[0:5]" -type "float3"  0 1.1175871e-07 0 0 1.1920929e-07 
		0 1.1273235 0.096968114 0 1.6364782 0.12120997 0 2.000108 -1.0430813e-07 0 1.1273242 
		-0.21817793 0;
	setAttr -s 6 ".vt[0:5]"  1 3 0 1 4 0 4.30295324 4.29083204 0 6.36352205 2.98176479 0
		 5.99989223 2.54540896 0 4.35143709 3.58781433 0;
	setAttr -s 6 ".ed[0:5]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 0 0;
	setAttr -ch 6 ".fc[0]" -type "polyFaces" 
		f 6 0 1 2 3 4 5
		mu 0 6 0 1 2 3 4 5
		mc 0 6 0 1 2 3 4 5;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_main_l_button";
	rename -uid "3C848313-4406-C233-B2ED-E6BDE102C2A8";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr -k on ".selectableItems" -type "string" "['brow_main_l']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_main_l_buttonShape" -p "brow_main_l_button";
	rename -uid "ACCD299E-4908-5F34-D4CB-6A9B5B6515A2";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.68373432755470276 0.36726847290992737 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0 0.2387 1 1 0 0.2387 1 1 0 0.2387
		 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  1.1266345 -3.9492207 0.16107436 
		1.431021 -3.829201 0.16107436 1.4320637 -3.5496144 0.16107436 1.2006795 -3.3161457 
		0.16107436 2.0362158 -3.1209798 0.16107436 1.9442264 -3.2108881 0.16107436 1.8960242 
		-3.7734284 0.16107436 1.9859334 -3.8418384 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_peak_l_button";
	rename -uid "F9304B11-4700-11C4-8906-64893EA55641";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr -k on ".selectableItems" -type "string" "['brow_peak_l']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_peak_l_buttonShape" -p "brow_peak_l_button";
	rename -uid "314010A2-46A1-45D3-EDD6-F59227BDC65C";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0 0.2387 1 1 0 0.2387 1 1 0 0.2387
		 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  3.2734823 -3.7780883 0.16107436 
		3.5519848 -3.6347024 0.16107436 3.5284052 -3.3563838 0.16107436 3.2736645 -3.1488006 
		0.16107436 2.9717629 -3.0780618 0.16107436 2.9056578 -3.1913261 0.16107436 2.8820782 
		-3.7526028 0.16107436 2.9953427 -3.7951307 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_inner_l_button";
	rename -uid "826686C7-4A8E-D526-67D8-76999CB861F0";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr -k on ".selectableItems" -type "string" "['brow_inner_l']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_inner_l_buttonShape" -p "brow_inner_l_button";
	rename -uid "7FCCAB9D-4117-FACD-50AF-5CA9912766BC";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 1 0.2916470468044281 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0 0.2387 1 1 0 0.2387 1 1 0 0.2387
		 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -0.68759525 -4.1185246 0.16107436 
		-0.39306068 -3.9901755 0.16107436 -0.40110999 -3.7113521 0.16107436 -0.64082301 -3.4877377 
		0.16107436 -0.54481792 -3.365519 0.16107436 -0.62695396 -3.4637508 0.16107436 -0.66606498 
		-4.0255337 0.16107436 -0.56783038 -4.0840893 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_corrugator_l_button";
	rename -uid "E89241C7-42E2-4404-CBB0-C6B13A1E22E6";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr -k on ".selectableItems" -type "string" "['brow_corrugator_l']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_corrugator_l_buttonShape" -p "brow_corrugator_l_button";
	rename -uid "F80CD428-4F9F-3E9F-F178-2A8EEF5801AC";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.49559542536735535 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0.88450003 0 1 1 0.88450003 0 1
		 1 0.88450003 0 1 1 0.88450003 0 1 1 0.88450003 0 1 1 0.88450003 0 1 1 0.88450003
		 0 1 1 0.88450003 0 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.44021946 -4.0322504 0.16107436 
		0.74422771 -3.9119141 0.16107436 0.74492484 -3.6323667 0.16107436 0.51323158 -3.3992789 
		0.16107436 0.18254745 -3.2997315 0.16107436 0.090937376 -3.3899438 0.16107436 0.04308027 
		-3.9524517 0.16107436 0.13329524 -4.0204821 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_peak_r_button";
	rename -uid "EC180923-43A8-9596-1387-FAA176B9521B";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr -k on ".selectableItems" -type "string" "['brow_peak_r']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_peak_r_buttonShape" -p "brow_peak_r_button";
	rename -uid "3A6F10AA-4047-D333-1E28-9B8806ED4DF5";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.49559542536735535 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0 0.2387 1 1 0 0.2387 1 1 0 0.2387
		 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  3.2734823 -3.7780883 0.16107436 
		3.5519848 -3.6347024 0.16107436 3.5284052 -3.3563838 0.16107436 3.2736645 -3.1488006 
		0.16107436 2.9717629 -3.0780618 0.16107436 2.9056578 -3.1913261 0.16107436 2.8820782 
		-3.7526028 0.16107436 2.9953427 -3.7951307 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_all_r_button";
	rename -uid "A4F6040B-419A-FA63-5519-EB91DEC9E8D8";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr -k on ".selectableItems" -type "string" "['brow_inner_r', 'brow_main_r', 'brow_peak_r']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_all_r_buttonShape" -p "brow_all_r_button";
	rename -uid "6C84929F-415F-47F3-D06E-DB826A533D26";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.040678106248378754 0.96610158681869507 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 6 ".uvst[0].uvsp[0:5]" -type "float2" 0.084756069 4.139903e-17
		 0.27120072 0 0.32542479 0.61581796 0.081356212 1 0 0.93220317 0.19435091 0.62485754;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 6 ".clst[0].clsp[0:5]"  0 0.61870003 1 1 0 0.61870003 1
		 1 0 0.61870003 1 1 0 0.61870003 1 1 0 0.61870003 1 1 0 0.61870003 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 6 ".pt[0:5]" -type "float3"  0 1.1175871e-07 0 0 1.1920929e-07 
		0 1.1273235 0.096968114 0 1.6364782 0.12120997 0 2.000108 -1.0430813e-07 0 1.1273242 
		-0.21817793 0;
	setAttr -s 6 ".vt[0:5]"  1 3 0 1 4 0 4.30295324 4.29083204 0 6.36352205 2.98176479 0
		 5.99989223 2.54540896 0 4.35143709 3.58781433 0;
	setAttr -s 6 ".ed[0:5]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 0 0;
	setAttr -ch 6 ".fc[0]" -type "polyFaces" 
		f 6 0 1 2 3 4 5
		mu 0 6 0 1 2 3 4 5
		mc 0 6 0 1 2 3 4 5;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_main_r_button";
	rename -uid "88C62430-4D52-378B-A966-13B0C2DA40EA";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr -k on ".selectableItems" -type "string" "['brow_main_r']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_main_r_buttonShape" -p "brow_main_r_button";
	rename -uid "B198E3E5-4C41-A93D-52DD-87A1536DD79E";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.68373432755470276 0.36726847290992737 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0 0.2387 1 1 0 0.2387 1 1 0 0.2387
		 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  1.1266345 -3.9492207 0.16107436 
		1.431021 -3.829201 0.16107436 1.4320637 -3.5496144 0.16107436 1.2006795 -3.3161457 
		0.16107436 2.0362158 -3.1209798 0.16107436 1.9442264 -3.2108881 0.16107436 1.8960242 
		-3.7734284 0.16107436 1.9859334 -3.8418384 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_corrugator_r_button";
	rename -uid "AFA1F89D-4184-1619-3935-399BA54FBF02";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr -k on ".selectableItems" -type "string" "['brow_corrugator_r']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_corrugator_r_buttonShape" -p "brow_corrugator_r_button";
	rename -uid "31AB89D5-48AB-0D19-B95D-9F8163FE5376";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.49559542536735535 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0.88450003 0 1 1 0.88450003 0 1
		 1 0.88450003 0 1 1 0.88450003 0 1 1 0.88450003 0 1 1 0.88450003 0 1 1 0.88450003
		 0 1 1 0.88450003 0 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.44021946 -4.0322504 0.16107436 
		0.74422771 -3.9119141 0.16107436 0.74492484 -3.6323667 0.16107436 0.51323158 -3.3992789 
		0.16107436 0.18254745 -3.2997315 0.16107436 0.090937376 -3.3899438 0.16107436 0.04308027 
		-3.9524517 0.16107436 0.13329524 -4.0204821 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "brow_inner_r_button";
	rename -uid "4315C55A-4A34-F234-8E09-E9AC06889C14";
	addAttr -ci true -sn "selectableItems" -ln "selectableItems" -dt "string";
	addAttr -ci true -sn "buttonType" -ln "buttonType" -dt "string";
	setAttr ".s" -type "double3" -1 1 1 ;
	setAttr -k on ".selectableItems" -type "string" "['brow_inner_r']";
	setAttr -k on ".buttonType" -type "string" "select";
createNode mesh -n "brow_inner_r_buttonShape" -p "brow_inner_r_button";
	rename -uid "A1516C83-42E1-BA8A-E2C9-C79C2EF868D1";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.49559542536735535 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 8 ".uvst[0].uvsp[0:7]" -type "float2" 0.36746866 0 0.80413383
		 7.5109985e-17 1 0.29164705 0.91089839 0.73453695 0.64437002 0.99119085 0.33534881
		 0.92212623 0 0.49554545 0.078550592 0.19934972;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".ccls" -type "string" "colorSet1";
	setAttr ".clst[0].clsn" -type "string" "colorSet1";
	setAttr -s 8 ".clst[0].clsp[0:7]"  0 0.2387 1 1 0 0.2387 1 1 0 0.2387
		 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1 0 0.2387 1 1;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -0.68759525 -4.1185246 0.16107436 
		-0.39306068 -3.9901755 0.16107436 -0.40110999 -3.7113521 0.16107436 -0.64082301 -3.4877377 
		0.16107436 -0.54481792 -3.365519 0.16107436 -0.62695396 -3.4637508 0.16107436 -0.66606498 
		-4.0255337 0.16107436 -0.56783038 -4.0840893 0.16107436;
	setAttr -s 8 ".vt[0:7]"  2 8 0 1.48106754 7.61618757 0 1.50464725 7.097435474 0
		 1.99981928 6.64942265 0 2.5421505 6.57868385 0 2.84868574 6.93237829 0 2.87226534 7.73408556 0
		 2.5185709 8.017041206 0;
	setAttr -s 8 ".ed[0:7]"  0 1 0 1 2 0 2 3 0 3 4 0 4 5 0 5 6 0 6 7 0
		 7 0 0;
	setAttr -ch 8 ".fc[0]" -type "polyFaces" 
		f 8 0 1 2 3 4 5 6 7
		mu 0 8 0 1 2 3 4 5 6 7
		mc 0 8 0 1 2 3 4 5 6 7;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -s 35 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 24 ".gn";
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "brow_all_l__buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_main_l_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_peak_l_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_inner_l_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_corrugator_l_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_peak_r_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_all_r_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_main_r_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_corrugator_r_buttonShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "brow_inner_r_buttonShape.iog" ":initialShadingGroup.dsm" -na;
// End of biped_picker.ma
