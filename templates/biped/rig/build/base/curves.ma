//Maya ASCII 2018ff08 scene
//Name: curves.ma
//Last modified: Sun, Sep 02, 2018 02:05:13 PM
//Codeset: 1252
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201804211841-f3d65dda2a";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "A6BE766E-4F3E-077A-C0A0-F588E48E9100";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1.9594551777988891 59.950325550517263 12.457547064181313 ;
	setAttr ".r" -type "double3" 2.6616472703974594 -4.5999999999998948 -4.985676158671617e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "9DB9679E-40E8-9DE0-ABC6-99A53B91673E";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 10.034608892250347;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 62.538616113586258 2.881884277425462 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "8ED79B2B-424D-812D-28C4-EAA50E957098";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "5EF56283-42A9-5572-3F6E-A2B999BC7587";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "A9EC0C76-4462-A404-FA74-A7ABEC9EA58E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "525F914C-492B-3DB4-4861-54B9658174A6";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "50BD0572-4937-B926-C44C-AFAFEE60C04B";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "917A1C11-4D05-AA4E-CE5B-9296BCA04D94";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "lidLower_curves";
	rename -uid "B98D65E2-44E9-536E-1D7B-0BA19A9F2C53";
createNode transform -n "lidLower_open_l_curve" -p "lidLower_curves";
	rename -uid "D986AE39-48F0-F3C7-20FD-6CA7B2542416";
createNode nurbsCurve -n "lidLower_open_l_curveShape" -p "lidLower_open_l_curve";
	rename -uid "C65DB264-41CA-62B9-5D8B-97B4DEEBD9C8";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.356711651173789 2.9932492307048753
		0.57486823608043081 62.202676986671079 3.0384998007304627
		0.78537842621522214 61.932348220635518 3.0172100891303226
		1.2547669305535176 61.772718588488353 2.9057136324621182
		1.6757742904874551 61.913087216614123 2.7533106657731126
		1.9331557959194421 62.226255827363673 2.5901554544720162
		1.9386597227718925 62.424325134461199 2.5876520884884142
		;
createNode transform -n "lidLower_closed_l_curve" -p "lidLower_curves";
	rename -uid "3CB9EE21-48C9-B476-2B17-BD9068AE9B0F";
createNode nurbsCurve -n "lidLower_closed_l_curveShape" -p "lidLower_closed_l_curve";
	rename -uid "50B39027-43B8-91DC-85FD-C09DC892110D";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57181793246688273 62.42473652635698 2.9931638474043463
		0.61216439912988319 62.644818586099824 2.9976281542913297
		0.79914154596129827 62.980488060778228 2.9875062452325216
		1.2492136022186031 63.138825801006966 2.9501296378788733
		1.6561087345151 63.006567745145887 2.7801503959923948
		1.9137586058589073 62.673557066240967 2.6521161121124108
		1.9274270774739226 62.457846133678338 2.6022342144621087
		;
createNode transform -n "lidLower_middle_l_curve" -p "lidLower_curves";
	rename -uid "A9D3C011-49B0-28DA-936E-8DADCA4F0991";
createNode nurbsCurve -n "lidLower_middle_l_curveShape" -p "lidLower_middle_l_curve";
	rename -uid "E8F30BF7-48A3-219C-57AA-38896174E55A";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.338055665637711 3.0078313566785697
		0.57302565617467871 62.400857370542852 3.0719219710192394
		0.79829303335512924 62.580863823462877 3.1865529018808734
		1.2547669305535176 62.591106475829406 3.1413111259356374
		1.6588853986825571 62.52839335593805 2.9559934512969224
		1.9222986511877216 62.436750370888525 2.7111080643536174
		1.9386597227718925 62.4133165949249 2.6022342144621087
		;
createNode transform -n "lidLower_neutral_l_curve" -p "lidLower_curves";
	rename -uid "18887A61-4ECB-774F-C9D0-D7A67199E276";
createNode nurbsCurve -n "lidLower_neutral_l_curveShape" -p "lidLower_neutral_l_curve";
	rename -uid "FDCBDD29-4195-1AEB-EDE5-42ACA2C20880";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".iog[0].og[11].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".iog[0].og[12].gcl" -type "componentList" 1 "cv[0:6]";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.353145052904431 2.9902567976937977
		0.62511317401001176 62.233568461969796 3.0065578578126329
		0.8000763324898077 62.033175163847268 2.9993042482662013
		1.2574418792555353 61.87268631915893 2.9188830450042835
		1.6553188004131993 62.031669253245568 2.8041391673497413
		1.879499471955433 62.260225962934982 2.6422226115592444
		1.915303261933079 62.394064563240697 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_neutral_l_curveShapeOrig" -p "lidLower_neutral_l_curve";
	rename -uid "FBB8D05F-4377-AA33-4C25-E59DC5BD5F08";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_neutral_l_curveShapeOrig1" -p "lidLower_neutral_l_curve";
	rename -uid "5EF3057B-412E-952B-4875-73B375CE9D9A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.353145052904431 2.9902567976937977
		0.62511317401001198 62.233568461969796 3.0065578578126329
		0.80007633248980792 62.033175163847268 2.9993042482662013
		1.2574418792555355 61.87268631915893 2.9188830450042835
		1.6553188004131996 62.031669253245568 2.8041391673497413
		1.8794994719554332 62.260225962934982 2.6422226115592444
		1.9377680732045532 62.429675031865237 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode transform -n "lidLower_blink_l_curve" -p "lidLower_curves";
	rename -uid "F81486C9-475E-ABA5-5315-5B9CBE3F83D0";
createNode nurbsCurve -n "lidLower_blink_l_curveShape" -p "lidLower_blink_l_curve";
	rename -uid "96B185DC-4D0A-DCED-A16E-55BE9F2AA89D";
	setAttr -k off ".v";
	setAttr ".iog[0].og[9].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.353145052904431 2.9902567976937977
		0.62511317401001198 62.233568461969796 3.0065578578126329
		0.80007633248980792 62.033175163847268 2.9993042482662013
		1.2574418792555355 61.87268631915893 2.9188830450042835
		1.6553188004131996 62.031669253245568 2.8041391673497413
		1.8794994719554332 62.260225962934982 2.6422226115592444
		1.915303261933079 62.394064563240697 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_blink_l_curveShapeOrig" -p "lidLower_blink_l_curve";
	rename -uid "81B4ACCD-4DBB-16C2-1F77-CFBB8367A048";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_blink_l_curveShapeOrig1" -p "lidLower_blink_l_curve";
	rename -uid "F54058F8-46B5-0377-C0E7-C3AB785707C7";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.353145052904431 2.9902567976937977
		0.62511317401001198 62.233568461969796 3.0065578578126329
		0.80007633248980792 62.033175163847268 2.9993042482662013
		1.2574418792555355 61.87268631915893 2.9188830450042835
		1.6553188004131996 62.031669253245568 2.8041391673497413
		1.8794994719554332 62.260225962934982 2.6422226115592444
		1.9377680732045532 62.429675031865237 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode transform -n "lidLower_blink_r_curve" -p "lidLower_curves";
	rename -uid "529999D8-4863-BB59-B4F8-30BD0A2D5638";
createNode nurbsCurve -n "lidLower_blink_r_curveShape" -p "lidLower_blink_r_curve";
	rename -uid "2EB35B00-4FA0-9323-A778-D8A6845B230C";
	setAttr -k off ".v";
	setAttr ".iog[0].og[9].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.353145052904431 2.9902567976937977
		-0.62511317401001198 62.233568461969796 3.0065578578126329
		-0.80007633248980792 62.033175163847268 2.9993042482662013
		-1.2574418792555355 61.87268631915893 2.9188830450042835
		-1.6553188004131996 62.031669253245568 2.8041391673497413
		-1.8794994719554332 62.260225962934982 2.6422226115592444
		-1.915303261933079 62.394064563240697 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_blink_r_curveShapeOrig" -p "lidLower_blink_r_curve";
	rename -uid "FB603AB5-468C-DBCB-90F4-95A41E2CC382";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_blink_r_curveShapeOrig1" -p "lidLower_blink_r_curve";
	rename -uid "F03DB528-4E68-E053-9529-60B9D9278698";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.353145052904431 2.9902567976937977
		0.62511317401001198 62.233568461969796 3.0065578578126329
		0.80007633248980792 62.033175163847268 2.9993042482662013
		1.2574418792555355 61.87268631915893 2.9188830450042835
		1.6553188004131996 62.031669253245568 2.8041391673497413
		1.8794994719554332 62.260225962934982 2.6422226115592444
		1.9377680732045532 62.429675031865237 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode transform -n "lidLower_neutral_r_curve" -p "lidLower_curves";
	rename -uid "6EC9C105-49F9-6153-07F2-69B0B2F6406D";
createNode nurbsCurve -n "lidLower_neutral_r_curveShape" -p "lidLower_neutral_r_curve";
	rename -uid "5F843795-488F-1F54-5131-0F9B7A6300F3";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".iog[0].og[11].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".iog[0].og[12].gcl" -type "componentList" 1 "cv[0:6]";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.353145052904431 2.9902567976937977
		-0.62511317401001176 62.233568461969796 3.0065578578126329
		-0.8000763324898077 62.033175163847268 2.9993042482662013
		-1.2574418792555353 61.87268631915893 2.9188830450042835
		-1.6553188004131993 62.031669253245568 2.8041391673497413
		-1.879499471955433 62.260225962934982 2.6422226115592444
		-1.915303261933079 62.394064563240697 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_neutral_r_curveShapeOrig" -p "lidLower_neutral_r_curve";
	rename -uid "1AB3B82E-4B69-74AE-E2C7-92B8A6CD9D6B";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidLower_neutral_r_curveShapeOrig1" -p "lidLower_neutral_r_curve";
	rename -uid "CACB0090-4398-A1EE-E207-ECB1C438AE15";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.353145052904431 2.9902567976937977
		0.62511317401001198 62.233568461969796 3.0065578578126329
		0.80007633248980792 62.033175163847268 2.9993042482662013
		1.2574418792555355 61.87268631915893 2.9188830450042835
		1.6553188004131996 62.031669253245568 2.8041391673497413
		1.8794994719554332 62.260225962934982 2.6422226115592444
		1.9377680732045532 62.429675031865237 2.5772156529700507
		;
	setAttr ".dcv" yes;
createNode transform -n "lidLower_middle_r_curve" -p "lidLower_curves";
	rename -uid "369AAF0F-4281-0796-A1F3-BB81591E869C";
createNode nurbsCurve -n "lidLower_middle_r_curveShape" -p "lidLower_middle_r_curve";
	rename -uid "DBC3078A-4454-A6E5-3812-C293C2F75F7C";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.338055665637711 3.0078313566785697
		-0.57302565617467871 62.400857370542852 3.0719219710192394
		-0.79829303335512924 62.580863823462877 3.1865529018808734
		-1.2547669305535176 62.591106475829406 3.1413111259356374
		-1.6588853986825571 62.52839335593805 2.9559934512969224
		-1.9222986511877216 62.436750370888525 2.7111080643536174
		-1.9386597227718925 62.4133165949249 2.6022342144621087
		;
createNode transform -n "lidLower_closed_r_curve" -p "lidLower_curves";
	rename -uid "45F38F1B-4726-5398-E593-36B98D985ACF";
createNode nurbsCurve -n "lidLower_closed_r_curveShape" -p "lidLower_closed_r_curve";
	rename -uid "DC43E868-4A3F-6816-1F8C-D78FD5CEBDAB";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57181793246688273 62.42473652635698 2.9931638474043463
		-0.61216439912988319 62.644818586099824 2.9976281542913297
		-0.79914154596129827 62.980488060778228 2.9875062452325216
		-1.2492136022186031 63.138825801006966 2.9501296378788733
		-1.6561087345151 63.006567745145887 2.7801503959923948
		-1.9137586058589073 62.673557066240967 2.6521161121124108
		-1.9274270774739226 62.457846133678338 2.6022342144621087
		;
createNode transform -n "lidLower_open_r_curve" -p "lidLower_curves";
	rename -uid "A8B32606-4C54-3C1C-14F0-D3AA1A07E2A9";
createNode nurbsCurve -n "lidLower_open_r_curveShape" -p "lidLower_open_r_curve";
	rename -uid "046EC47E-4086-E6A5-0696-A2B3A654D93D";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.356711651173789 2.9932492307048753
		-0.57486823608043081 62.202676986671079 3.0384998007304627
		-0.78537842621522214 61.932348220635518 3.0172100891303226
		-1.2547669305535176 61.772718588488353 2.9057136324621182
		-1.6757742904874551 61.913087216614123 2.7533106657731126
		-1.9331557959194421 62.226255827363673 2.5901554544720162
		-1.9386597227718925 62.424325134461199 2.5876520884884142
		;
createNode transform -n "lidUpper_curves";
	rename -uid "63297D63-456A-66A7-9383-A5A03FB513E3";
createNode transform -n "lidUpper_open_l_curve" -p "lidUpper_curves";
	rename -uid "7CDC18BF-46EC-0353-4F7C-B59531B035CF";
createNode nurbsCurve -n "lidUpper_open_l_curveShape" -p "lidUpper_open_l_curve";
	rename -uid "255D0206-4B70-5C66-119D-EB80504650D3";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.55436029603162595 62.653539852542934 3.0384998007304627
		0.78537842621522214 63.146090355951621 3.0172100891303226
		1.2547669305535176 63.304513638684156 2.9057136324621182
		1.6588853986825571 63.1207164316315 2.7533106657731126
		1.9222986511877216 62.708109502602319 2.5901554544720162
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
createNode transform -n "lidUpper_closed_l_curve" -p "lidUpper_curves";
	rename -uid "DD8A356B-4104-D1C2-428E-A6A4ED6091E8";
createNode nurbsCurve -n "lidUpper_closed_l_curveShape" -p "lidUpper_closed_l_curve";
	rename -uid "E5F06CB2-4A29-B942-778D-36889288F717";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.58336912708870126 62.315842352298048 2.9931638474043463
		0.65632558119839524 62.18415646344009 2.9976281542913297
		0.83161300336461597 62.009865117770659 2.9875062452325216
		1.2492136022186031 61.887739750750846 2.9501296378788733
		1.6561087345151 62.00333806036771 2.7801503959923948
		1.8838848650478548 62.268082410705027 2.6521161121124108
		1.9166518939707227 62.383113413461992 2.6022342144621087
		;
createNode transform -n "lidUpper_middle_l_curve" -p "lidUpper_curves";
	rename -uid "BCE48602-4391-F143-7BA0-5FA759E5889F";
createNode nurbsCurve -n "lidUpper_middle_l_curveShape" -p "lidUpper_middle_l_curve";
	rename -uid "26D8F0FE-4149-214D-BD3D-1D9CF4579A76";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.338055665637711 3.0078313566785697
		0.57302565617467871 62.400857370542852 3.0719219710192394
		0.79829303335512924 62.580863823462877 3.1865529018808734
		1.2547669305535176 62.591106475829406 3.1413111259356374
		1.6588853986825571 62.52839335593805 2.9559934512969224
		1.9222986511877216 62.436750370888525 2.7111080643536174
		1.9386597227718925 62.4133165949249 2.6022342144621087
		;
createNode transform -n "lidUpper_neutral_l_curve" -p "lidUpper_curves";
	rename -uid "C3E8B681-41A8-7BD0-C92E-B9ABA2724EFB";
createNode nurbsCurve -n "lidUpper_neutral_l_curveShape" -p "lidUpper_neutral_l_curve";
	rename -uid "83397C9C-45CB-24CC-E4CE-D1AA1436D48E";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".iog[0].og[2].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".iog[0].og[3].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467849 62.624485228401319 3.0384998007304627
		0.79829303335512902 62.97912399483311 3.0172100891303226
		1.2547669305535174 63.132918067724333 2.9743518608460469
		1.6588853986825569 63.002029495050955 2.846258266709683
		1.9222986511877214 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidUpper_neutral_l_curveShapeOrig" -p "lidUpper_neutral_l_curve";
	rename -uid "8D93F912-4601-49ED-98E8-35A43117682A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode transform -n "lidUpper_blink_l_curve" -p "lidUpper_curves";
	rename -uid "CB1D808C-49AE-8289-944F-D18965865D90";
createNode nurbsCurve -n "lidUpper_blink_l_curveShape" -p "lidUpper_blink_l_curve";
	rename -uid "89C160B6-427A-C1AD-57F8-93BF567AD493";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514355 62.367219917585096 2.9932492307048739
		0.57302565617467938 62.62448522840134 3.0384998007304636
		0.79829303335512947 62.97912399483311 3.0172100891303213
		1.254766930553515 63.132918067724333 2.9743518608460375
		1.6588853986825576 63.002029495050948 2.8462582667096816
		1.9222986511877203 62.678080277684344 2.6359142733946355
		1.9386597227718929 62.442480846872293 2.5876520884884155
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidUpper_blink_l_curveShapeOrig" -p "lidUpper_blink_l_curve";
	rename -uid "68C45E35-4CEE-4B07-A5DD-D58EC9D3E3FE";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode transform -n "lidUpper_open_r_curve" -p "lidUpper_curves";
	rename -uid "D0038903-458D-068A-43C4-D8827B57E7E5";
createNode nurbsCurve -n "lidUpper_open_r_curveShape" -p "lidUpper_open_r_curve";
	rename -uid "38A4B678-4EF2-52ED-846D-A0BCA0951263";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.367219917585096 2.9932492307048753
		-0.55436029603162595 62.653539852542934 3.0384998007304627
		-0.78537842621522214 63.146090355951621 3.0172100891303226
		-1.2547669305535176 63.304513638684156 2.9057136324621182
		-1.6588853986825571 63.1207164316315 2.7533106657731126
		-1.9222986511877216 62.708109502602319 2.5901554544720162
		-1.9386597227718925 62.442480846872286 2.5876520884884142
		;
createNode transform -n "lidUpper_closed_r_curve" -p "lidUpper_curves";
	rename -uid "31A56D22-4E05-7750-904D-13B28415066F";
createNode nurbsCurve -n "lidUpper_closed_r_curveShape" -p "lidUpper_closed_r_curve";
	rename -uid "6B372D02-41C5-7BD3-AAB4-6CB2E6EB76B0";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.58336912708870126 62.315842352298048 2.9931638474043463
		-0.65632558119839524 62.18415646344009 2.9976281542913297
		-0.83161300336461597 62.009865117770659 2.9875062452325216
		-1.2492136022186031 61.887739750750846 2.9501296378788733
		-1.6561087345151 62.00333806036771 2.7801503959923948
		-1.8838848650478548 62.268082410705027 2.6521161121124108
		-1.9166518939707227 62.383113413461992 2.6022342144621087
		;
createNode transform -n "lidUpper_middle_r_curve" -p "lidUpper_curves";
	rename -uid "DE392635-40E4-B987-EED1-3A8260015046";
createNode nurbsCurve -n "lidUpper_middle_r_curveShape" -p "lidUpper_middle_r_curve";
	rename -uid "428E1F15-4AA9-0CF3-A23A-B5BD2FF4D0F2";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.338055665637711 3.0078313566785697
		-0.57302565617467871 62.400857370542852 3.0719219710192394
		-0.79829303335512924 62.580863823462877 3.1865529018808734
		-1.2547669305535176 62.591106475829406 3.1413111259356374
		-1.6588853986825571 62.52839335593805 2.9559934512969224
		-1.9222986511877216 62.436750370888525 2.7111080643536174
		-1.9386597227718925 62.4133165949249 2.6022342144621087
		;
createNode transform -n "lidUpper_neutral_r_curve" -p "lidUpper_curves";
	rename -uid "33F3DC8D-40C4-7466-B728-A6A9826EB834";
createNode nurbsCurve -n "lidUpper_neutral_r_curveShape" -p "lidUpper_neutral_r_curve";
	rename -uid "96A20A3F-4781-F677-535B-6EBED8024AC9";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".iog[0].og[2].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".iog[0].og[3].gcl" -type "componentList" 1 "cv[*]";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514367 62.367219917585096 2.9932492307048753
		-0.57302565617467849 62.624485228401319 3.0384998007304627
		-0.79829303335512902 62.97912399483311 3.0172100891303226
		-1.2547669305535174 63.132918067724333 2.9743518608460469
		-1.6588853986825569 63.002029495050955 2.846258266709683
		-1.9222986511877214 62.678080277684352 2.6359142733946355
		-1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidUpper_neutral_r_curveShapeOrig" -p "lidUpper_neutral_r_curve";
	rename -uid "94AF9937-4F06-1571-D926-6AB00726BA25";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode transform -n "lidUpper_blink_r_curve" -p "lidUpper_curves";
	rename -uid "10C5A02B-48E5-1545-DBD4-D99BBD8D8B9E";
createNode nurbsCurve -n "lidUpper_blink_r_curveShape" -p "lidUpper_blink_r_curve";
	rename -uid "9F91B8F2-4152-72EA-AB4E-C8AAA8FF5155";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		-0.57087413833514355 62.367219917585096 2.9932492307048739
		-0.57302565617467938 62.62448522840134 3.0384998007304636
		-0.79829303335512947 62.97912399483311 3.0172100891303213
		-1.254766930553515 63.132918067724333 2.9743518608460375
		-1.6588853986825576 63.002029495050948 2.8462582667096816
		-1.9222986511877203 62.678080277684344 2.6359142733946355
		-1.9386597227718929 62.442480846872293 2.5876520884884155
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lidUpper_blink_r_curveShapeOrig" -p "lidUpper_blink_r_curve";
	rename -uid "4B6A31AE-4CD5-3635-17B9-EEAB35DDC838";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		2 5 0 no 3
		8 0 0 1 2 3 4 5 5
		7
		0.57087413833514367 62.367219917585096 2.9932492307048753
		0.57302565617467871 62.624485228401319 3.0384998007304627
		0.79829303335512924 62.97912399483311 3.0172100891303226
		1.2547669305535176 63.132918067724333 2.9743518608460469
		1.6588853986825571 63.002029495050955 2.846258266709683
		1.9222986511877216 62.678080277684352 2.6359142733946355
		1.9386597227718925 62.442480846872286 2.5876520884884142
		;
	setAttr ".dcv" yes;
createNode transform -n "lip_main_curve";
	rename -uid "D64D381C-42C7-AD00-6C9F-6EA5D9811804";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "lip_main_curveShape" -p "lip_main_curve";
	rename -uid "BE16FA0C-45B8-2060-5767-63A8CA00B6B1";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 16 2 no 3
		21 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
		19
		0.52920153965296279 59.17559050183263 4.010393969411453
		-4.1824262471307082e-16 59.178588925034639 4.2717508457819449
		-0.52920229899051585 59.175588789689392 4.0103955135818934
		-0.97783801486183108 59.168838493207467 3.6925559557309597
		-1.1626231671032699 59.153984158315623 3.472230852347721
		-1.3828695672304363 59.128499958246579 3.2213397204382197
		-1.162623051460173 59.100021287030032 3.4684271955998653
		-0.97783893334322869 59.068202964643014 3.6925522809271314
		-0.52920229899051552 59.034249003830496 3.9757415079826623
		-1.9491397643692446e-16 59.023177908846833 4.2025945075883087
		0.52920244240609193 59.034248368612559 3.9757422673878651
		0.97783791345528925 59.068202980181212 3.6925508243762124
		1.1626222491349907 59.100021287030046 3.4684262834079576
		1.3828717653616849 59.128547626703636 3.2213447128063954
		1.1626221065698275 59.153984158315637 3.4722296324352158
		0.97783885097388179 59.168838508745665 3.6925571498227114
		0.52920153965296279 59.17559050183263 4.010393969411453
		-4.1824262471307082e-16 59.178588925034639 4.2717508457819449
		-0.52920229899051585 59.175588789689392 4.0103955135818934
		;
	setAttr ".dcv" yes;
createNode nurbsCurve -n "lip_main_curveShapeOrig" -p "lip_main_curve";
	rename -uid "7E7F8E2E-425C-79CE-1C5A-DB9CEDF2020C";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".cc" -type "nurbsCurve" 
		3 16 2 no 3
		21 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
		19
		0.52920229899051485 59.175588789689392 4.0103955135818934
		4.0505543140516046e-16 59.178589351085101 4.1640687567302104
		-0.52920229899051585 59.175588789689392 4.0103955135818934
		-0.97783834519051172 59.168839229835001 3.6925567362237905
		-1.1626227043903505 59.153983258634923 3.4722302844905482
		-1.3828722495768861 59.128547153886707 3.2213449060615282
		-1.1626227043903501 59.100020752732974 3.4684266291320855
		-0.97783834519051172 59.068202083351935 3.6925517178135721
		-0.52920229899051552 59.034249003830496 3.9757415079826623
		1.8172675256351429e-16 59.023179369855576 4.0949113835782915
		0.52920229899051596 59.034249003830496 3.9757415079826623
		0.97783834519051149 59.068202083351935 3.6925517178135721
		1.1626227043903508 59.100020752732974 3.4684266291320855
		1.3828722495768857 59.128547153886707 3.2213449060615282
		1.1626227043903505 59.153983258634923 3.4722302844905482
		0.97783834519051127 59.168839229835001 3.6925567362237905
		0.52920229899051485 59.175588789689392 4.0103955135818934
		4.0505543140516046e-16 59.178589351085101 4.1640687567302104
		-0.52920229899051585 59.175588789689392 4.0103955135818934
		;
	setAttr ".dcv" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "6535346C-44FE-F04F-A7F4-07AB4C2C8080";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "29768FFB-4A72-2CA5-B5EA-AF890F67EFDD";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "685C508C-4AC7-AA15-AC22-63A49460A5F7";
createNode displayLayerManager -n "layerManager";
	rename -uid "43A3AE37-451B-5B67-7042-64B902F87CBA";
createNode displayLayer -n "defaultLayer";
	rename -uid "89B932C6-4ECB-D98E-D338-33B84B16E62F";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "780E517B-43B1-F406-31B6-66B9EB467C07";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "16324D1C-42F6-4900-04A2-DA8014634C22";
	setAttr ".g" yes;
createNode displayLayer -n "blink_curves_defaultLayer";
	rename -uid "29F590CE-4A44-26A5-F773-1DA9DC5310C1";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "0F50EDFA-4D7E-0650-3CEB-03A94FE63FFD";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n"
		+ "            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n"
		+ "            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n"
		+ "            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n"
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1720\n            -height 1304\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n"
		+ "            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n"
		+ "            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n"
		+ "                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n"
		+ "                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n"
		+ "                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n"
		+ "                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n"
		+ "                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n"
		+ "                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n"
		+ "                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1720\\n    -height 1304\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1720\\n    -height 1304\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "7B957B19-4E2E-1FDB-70D2-8C846E2D3863";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
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
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of curves.ma
