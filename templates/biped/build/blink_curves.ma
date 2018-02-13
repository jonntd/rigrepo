//Maya ASCII 2018 scene
//Name: blink_curves.ma
//Last modified: Mon, Feb 12, 2018 11:55:47 PM
//Codeset: 1252
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201706261615-f9658c4cfc";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "lidLower_curves";
	rename -uid "F3D5553F-4B84-2737-4F9D-538F65799F69";
createNode transform -n "lidLower_open_l_curve" -p "lidLower_curves";
	rename -uid "F51C3723-4F3D-8D65-F6BA-DE945AAFB876";
createNode nurbsCurve -n "lidLower_open_l_curveShape" -p "lidLower_open_l_curve";
	rename -uid "1DC6D837-407B-8E66-485B-4F9918C07AD6";
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
	rename -uid "ABF2F197-45DA-0D02-BEE1-E8BF1D26E9A5";
createNode nurbsCurve -n "lidLower_closed_l_curveShape" -p "lidLower_closed_l_curve";
	rename -uid "210D45B1-496B-833D-0EEF-5388463B3948";
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
	rename -uid "F8436D01-48B3-1B57-5D44-FFBD5F4CFFAF";
createNode nurbsCurve -n "lidLower_middle_l_curveShape" -p "lidLower_middle_l_curve";
	rename -uid "B300ED0D-4DB8-6349-9AF0-DF9FA4CC59D7";
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
	rename -uid "447ADC0F-4CE6-AFAD-D6EC-04BFB418D2CD";
createNode nurbsCurve -n "lidLower_neutral_l_curveShape" -p "lidLower_neutral_l_curve";
	rename -uid "D0C6C86E-40AD-7994-2AC2-9C91FD5348EA";
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
	rename -uid "5B79BA72-4640-774F-8283-D99C3597C59E";
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
createNode nurbsCurve -n "lidLower_neutral_l_curveShapeOrig2" -p "lidLower_neutral_l_curve";
	rename -uid "4B1ABA00-45DF-0EAB-25A0-479A88682215";
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
	rename -uid "BB509F45-41BB-ED3A-5A31-FDB61BD7C9A6";
createNode nurbsCurve -n "lidLower_blink_l_curveShape" -p "lidLower_blink_l_curve";
	rename -uid "5A3BE873-439E-E5D9-0E9F-81A92A071A2E";
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
	rename -uid "87DDDF4F-43BF-12C2-223D-FF893F43776C";
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
createNode nurbsCurve -n "lidLower_blink_l_curveShapeOrig2" -p "lidLower_blink_l_curve";
	rename -uid "65CFB096-46FB-60BA-80F4-339329789D34";
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
	rename -uid "21612C64-4C18-207E-FFB7-FC9BC1E64D69";
createNode nurbsCurve -n "lidLower_blink_r_curveShape" -p "lidLower_blink_r_curve";
	rename -uid "50369C07-4CE8-2F40-5A43-A89BFD93A70E";
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
	rename -uid "C2BBD7AE-4D66-DE79-64C4-08A087B0EA2A";
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
createNode nurbsCurve -n "lidLower_blink_r_curveShapeOrig3" -p "lidLower_blink_r_curve";
	rename -uid "F70EC77B-4EDF-6D28-E21B-A8911373CF0E";
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
	rename -uid "261CC7A1-4714-E229-CEC2-A4A8BBF4B485";
createNode nurbsCurve -n "lidLower_neutral_r_curveShape" -p "lidLower_neutral_r_curve";
	rename -uid "69E2AC7B-42FC-F9FF-D7AF-4A8A34052674";
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
	rename -uid "256B1DA2-49CC-640D-A3AD-4D9AD159CF1E";
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
createNode nurbsCurve -n "lidLower_neutral_r_curveShapeOrig3" -p "lidLower_neutral_r_curve";
	rename -uid "CE45CCA0-41FD-E5B3-A973-37947FBC7ED0";
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
	rename -uid "B890B4C6-47D6-DAEC-6BE7-D9A3E8B28590";
createNode nurbsCurve -n "lidLower_middle_r_curveShape" -p "lidLower_middle_r_curve";
	rename -uid "1FC29FED-4707-9E09-2479-899D34472834";
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
	rename -uid "2B53F7F6-45F3-6B06-2C90-0BB0FE205809";
createNode nurbsCurve -n "lidLower_closed_r_curveShape" -p "lidLower_closed_r_curve";
	rename -uid "22625273-464E-C186-0403-978DCEE9FBDD";
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
	rename -uid "E387E4E8-4979-0C75-7351-9EA543EE2ABF";
createNode nurbsCurve -n "lidLower_open_r_curveShape" -p "lidLower_open_r_curve";
	rename -uid "A8E7970A-406C-6DB3-FDBB-C399C508195B";
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
	rename -uid "2F582D72-47B3-61E2-C552-B49C0CD0E354";
createNode transform -n "lidUpper_open_l_curve" -p "lidUpper_curves";
	rename -uid "8278C705-473B-5738-D246-34B80373E400";
createNode nurbsCurve -n "lidUpper_open_l_curveShape" -p "lidUpper_open_l_curve";
	rename -uid "FD57A089-474F-EA1C-859B-418069BC2899";
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
	rename -uid "0109B004-46B2-14AB-B4CA-D0A707AFC551";
createNode nurbsCurve -n "lidUpper_closed_l_curveShape" -p "lidUpper_closed_l_curve";
	rename -uid "771CDB4F-40D4-BF64-86D5-4EBBD102CB25";
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
	rename -uid "6D3109F9-418B-117C-758C-D69035455A75";
createNode nurbsCurve -n "lidUpper_middle_l_curveShape" -p "lidUpper_middle_l_curve";
	rename -uid "5A0FF9AE-45D7-F9E9-3562-FDA2BF08D6CB";
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
	rename -uid "D4897E18-4948-95E6-3CE5-77B13659B16B";
createNode nurbsCurve -n "lidUpper_neutral_l_curveShape" -p "lidUpper_neutral_l_curve";
	rename -uid "0DE4D44A-48B7-B558-DCE6-50B8F3AEC3EE";
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
	rename -uid "4B70AC28-4BB0-E239-0172-F18D40D12081";
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
	rename -uid "5609D681-4E14-BAE5-63B8-C49B1FB277EB";
createNode nurbsCurve -n "lidUpper_blink_l_curveShape" -p "lidUpper_blink_l_curve";
	rename -uid "5590E6CE-4F29-844A-F7FB-0385B6A09DA4";
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
	rename -uid "02735EDA-452F-FA5E-5303-F2981A6EA1ED";
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
	rename -uid "42DF8325-49EE-ECDB-6A15-F5AF8BF8242A";
createNode nurbsCurve -n "lidUpper_open_r_curveShape" -p "lidUpper_open_r_curve";
	rename -uid "C7FC219C-48A1-7FCC-CC4B-489E86C7B72B";
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
	rename -uid "434F2FF3-490F-90CE-ED02-D9BF28888C62";
createNode nurbsCurve -n "lidUpper_closed_r_curveShape" -p "lidUpper_closed_r_curve";
	rename -uid "E8C01334-42B9-1D66-8232-8C89BE685060";
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
	rename -uid "42C287D0-46FE-1C92-F854-64B1E1D9B6D1";
createNode nurbsCurve -n "lidUpper_middle_r_curveShape" -p "lidUpper_middle_r_curve";
	rename -uid "68CDB872-47E6-66CD-780F-1F9FBEFFA41A";
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
	rename -uid "30EE9534-40C8-74E7-7156-369F0675FD37";
createNode nurbsCurve -n "lidUpper_neutral_r_curveShape" -p "lidUpper_neutral_r_curve";
	rename -uid "4DE679C6-4106-32D1-702A-908687D66D06";
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
	rename -uid "D1A6E81C-4E78-0D99-A046-9184AACD3E7A";
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
	rename -uid "663DAC6B-4ED3-9975-6B3B-1D9C78348434";
createNode nurbsCurve -n "lidUpper_blink_r_curveShape" -p "lidUpper_blink_r_curve";
	rename -uid "8F7C6443-459F-1CE1-E866-85BD5D2A28BF";
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
	rename -uid "40473FFB-4245-023C-5D8C-498FD8CE33DB";
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
createNode transform -s -n "persp";
	rename -uid "4C582DD9-4DD1-D57A-B30E-FC8F09FAFA9D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 2.0416963130270238 79.230860751113468 149.94984367471338 ;
	setAttr ".r" -type "double3" -15.938352729602443 0.19999999999993795 -7.4544704498650893e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "3AB8D931-4CE7-2B0D-0F93-D59405FFC4B9";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 149.80694666438592;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 1.2465100094017594 62.538616113586258 2.881884277425462 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "C3D52B8C-4FF9-0AB1-FB49-C48FB75A71DA";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "C45DF90E-468F-5FD6-0ABB-748308F5B27B";
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
	rename -uid "CAF41A98-4F07-8F3D-F94E-80B368F0B1B4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "536C5353-4482-0B99-E531-43A1F26DB653";
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
	rename -uid "2D7E8CD9-4FB8-2C1C-A9CF-3D995DC276E8";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "FC695F10-4158-D268-0FF2-DA88306EF43B";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "0E732AA8-49F2-4FB1-D193-08B15D39670E";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "276CC152-4022-D6CD-53EB-F997B4616275";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "39E1F2B8-4ED3-C37B-5D5F-34BF40B3C5BB";
createNode displayLayerManager -n "layerManager";
	rename -uid "C2500E42-43F3-31D3-D291-19B0C4503DEB";
createNode displayLayer -n "defaultLayer";
	rename -uid "B124963F-4CD1-11A1-CA97-6CB10A26ADA6";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "44308B96-4B6B-0CB6-FA71-E48216B36CA6";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "B6EF696B-4BDC-CB85-BE5A-79AE7AE9AA35";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "33411C57-45A4-99C1-D5A5-1180D109ADD7";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n"
		+ "            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n"
		+ "            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n"
		+ "            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n"
		+ "            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n"
		+ "            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 2357\n            -height 1047\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n"
		+ "            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n"
		+ "            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n"
		+ "            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n"
		+ "            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n"
		+ "                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n"
		+ "            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n"
		+ "                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n"
		+ "                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n"
		+ "            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n"
		+ "                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n"
		+ "                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n"
		+ "                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n"
		+ "                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n"
		+ "            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n"
		+ "            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n"
		+ "                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -highlightConnections 0\n                -copyConnectionsOnPaste 0\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n"
		+ "        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2357\\n    -height 1047\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n  \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2357\\n    -height 1047\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "E08D0D78-469D-9787-44A8-B68196536CCF";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 5;
	setAttr -av ".unw" 5;
	setAttr -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".etmr" no;
	setAttr ".tmr" 4096;
	setAttr ".aoon" yes;
	setAttr -av ".aoam" 0.52447551488876343;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr ".ai_surface_shader" -type "float3" -8.196107e+31 8.1275311e-43 0 ;
	setAttr ".ai_volume_shader" -type "float3" -8.196107e+31 8.1275311e-43 0 ;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr ".ai_surface_shader" -type "float3" -8.196107e+31 8.1275311e-43 0 ;
	setAttr ".ai_volume_shader" -type "float3" -8.196107e+31 8.1275311e-43 0 ;
select -ne :defaultRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr -k on ".edl";
	setAttr -cb on ".ren";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -cb on ".imfkey";
	setAttr -k on ".gama";
	setAttr -k on ".an";
	setAttr -cb on ".ar";
	setAttr -k on ".fs";
	setAttr -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -cb on ".me";
	setAttr -cb on ".se";
	setAttr -k on ".be";
	setAttr -cb on ".ep";
	setAttr -k on ".fec";
	setAttr -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -k on ".pff";
	setAttr -cb on ".peie";
	setAttr -k on ".ifp";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -k on ".shs";
	setAttr -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -k on ".mm";
	setAttr -k on ".npu" 11;
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -cb on ".prm";
	setAttr -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -k on ".ope";
	setAttr -k on ".oppf";
	setAttr -cb on ".hbl";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -k on ".isu";
	setAttr -k on ".pdu";
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
	setAttr ".cfp" -type "string" "/usr/share/colortools/config/default.ocio";
	setAttr ".ovt" no;
	setAttr ".povt" no;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off ".ctrs" 256;
	setAttr -av -k off ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :ikSystem;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av ".gsn";
	setAttr -k on ".gsv";
	setAttr -s 4 ".sol";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of blink_curves.ma
