//Maya ASCII 2018ff07 scene
//Name: skeleton.ma
//Last modified: Sun, Mar 11, 2018 11:09:29 PM
//Codeset: 1252
requires maya "2018ff07";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201711281015-8e846c9074";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "57FC3D85-424C-2215-74B6-C18C84B024AB";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 18.550414785109965 80.963653495656615 80.366517268825817 ;
	setAttr ".r" -type "double3" -12.938352729602492 12.600000000000023 2.036901868521717e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "D6326EAF-42B8-E42D-CA59-29A09EBD8006";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 82.403574569574516;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 1.0310094356536861 62.513282775878906 1.9892032146453853 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "A5210B40-41D3-4DAF-3C28-0DBAE4579988";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "E21B0571-4735-39A7-B036-4F8A80C1490F";
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
	rename -uid "0C1FCDD6-429F-2E65-61C2-0BA1FD4A749A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "CE1D6AC7-4302-3785-5969-03A254186008";
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
	rename -uid "1250E04B-44A1-52B8-435B-0087AD7FC602";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "76763E5D-49E4-5770-961F-B5B6C732E800";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "ankle_l_pivot";
	rename -uid "AD0B8FD1-43E5-8F39-0A2F-8696399A2A6E";
	setAttr ".t" -type "double3" 2.0709593296051025 2.3200583457946777 -0.38717499375343323 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.72642886516149041;
createNode joint -n "bankIn_l_pivot" -p "ankle_l_pivot";
	rename -uid "D620F80F-40A3-BCA9-178F-F0A1FEEF9659";
	setAttr ".t" -type "double3" -2.0709593296051021 -2.3200583457946777 4.3871749937534323 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.7068965517241379;
createNode joint -n "bankOut_l_pivot" -p "bankIn_l_pivot";
	rename -uid "BEAA8B09-47DA-42DB-54E4-1D90F2785DAC";
	setAttr ".t" -type "double3" 5 -1.5512182146406965e-31 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.74987682214717077;
createNode joint -n "heel_l_pivot" -p "bankOut_l_pivot";
	rename -uid "83C7FAE1-4154-5662-500D-E2ACF537653E";
	setAttr ".t" -type "double3" -3.0000000000000018 -1.5723961353091999e-15 -5.0000000000000009 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.72513256258997583;
createNode joint -n "ball_l_pivot" -p "heel_l_pivot";
	rename -uid "0009314F-4A45-A328-CEE2-119103FCA8DB";
	setAttr ".t" -type "double3" 0.070959329605103871 0.83647328615188754 5.2863225936889666 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "toe_l_pivot" -p "ball_l_pivot";
	rename -uid "DC0BFD9A-492C-E13A-FB94-1F8460AB253D";
	setAttr ".t" -type "double3" -0.070959329605101651 -0.8364732861518831 3.713677406311036 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "toeBend_l_pivot" -p "toe_l_pivot";
	rename -uid "5B83E7D0-40D1-3600-4D9D-63A0BF6085A6";
	setAttr ".t" -type "double3" 0.070959329605101651 0.8364732861518831 -3.713677406311036 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "ballRoll_l_pivot" -p "toe_l_pivot";
	rename -uid "C4A56C7B-42F4-7551-BA83-A6A8AF6DBAE3";
	setAttr ".t" -type "double3" 0.070959329605101651 0.8364732861518831 -3.713677406311036 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "ankle_r_pivot";
	rename -uid "6E19B685-4C1E-2B50-7F9E-CDA2852D28D3";
	setAttr ".t" -type "double3" -2.07096 2.32006 -0.387175 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.72642886516149041;
createNode joint -n "bankIn_r_pivot" -p "ankle_r_pivot";
	rename -uid "D76E08A0-4D1D-A438-034A-9899B2B2AA39";
	setAttr ".t" -type "double3" 2.0709599999999995 -2.32006 4.387175 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.7068965517241379;
createNode joint -n "bankOut_r_pivot" -p "bankIn_r_pivot";
	rename -uid "0F83718C-4376-85DF-3326-C4BCF34E6E5F";
	setAttr ".t" -type "double3" -5 -1.5512200000000002e-31 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.74987682214717077;
createNode joint -n "heel_r_pivot" -p "bankOut_r_pivot";
	rename -uid "626956ED-4FF6-E557-5EAC-EB996333AC45";
	setAttr ".t" -type "double3" 3 -1.5723999999999999e-15 -5 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.72513256258997583;
createNode joint -n "ball_r_pivot" -p "heel_r_pivot";
	rename -uid "F355B104-4F46-E0C3-85F9-8F8675875FC9";
	setAttr ".t" -type "double3" -0.070959999999999912 0.83647300000000158 5.28632 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "toe_r_pivot" -p "ball_r_pivot";
	rename -uid "4886394D-4ACD-2EF5-9006-6B9AA1735C3D";
	setAttr ".t" -type "double3" 0.070959999999999912 -0.83647299999999714 3.71368 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "ballRoll_r_pivot" -p "toe_r_pivot";
	rename -uid "36AAB11F-48A2-47AB-1DFC-5D9D83D5CECB";
	setAttr ".t" -type "double3" -0.070959999999999912 0.83647299999999714 -3.71368 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode joint -n "toeBend_r_pivot" -p "toe_r_pivot";
	rename -uid "8A22148A-4A13-D8F4-8FF9-6A944A25F3EA";
	setAttr ".t" -type "double3" -0.070959999999999912 0.83647299999999714 -3.71368 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60026110416454692;
createNode transform -n "bind";
	rename -uid "9372F699-41BB-898C-B462-C4BA6F26D957";
	setAttr ".dla" yes;
createNode joint -n "hips_bind" -p "bind";
	rename -uid "F31BD5F3-4B03-65F9-2782-18A96A3136D1";
	setAttr ".t" -type "double3" 1.8748704314691949e-32 39.26684153690082 0.30860046773316835 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.999999999999986 0 89.999999999999986 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".ds" 1;
	setAttr ".radi" 0.5;
createNode joint -n "spine_0_bind" -p "hips_bind";
	rename -uid "11275D59-4622-9545-0253-50A78F9B4427";
	setAttr ".t" -type "double3" -2.1461748457901635 2.7755575615628914e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.6498000615042016e-30 1.2722218725854064e-14 -6.3611093629270367e-15 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.77736256464791142;
createNode joint -n "spine_1_bind" -p "spine_0_bind";
	rename -uid "093E3DA9-4195-372D-96D8-A19FB15A3EE8";
	setAttr ".t" -type "double3" 2.1461748457901635 -1.1102230246251565e-16 -3.3618386580217053e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.76324381476434067;
createNode joint -n "spine_2_bind" -p "spine_1_bind";
	rename -uid "EFD0E113-4C86-E821-2B28-7DBA7D8B97F9";
	setAttr ".t" -type "double3" 2.1461748457901635 5.5511151231257827e-17 5.9386118465965891e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.77463874694409751;
createNode joint -n "spine_3_bind" -p "spine_2_bind";
	rename -uid "334873BD-443D-25D4-E232-E780D135610E";
	setAttr ".t" -type "double3" 2.1461748457901635 0 6.1246275110827068e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 0.47060966426211664 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.69305993203988836;
createNode joint -n "spine_4_bind" -p "spine_3_bind";
	rename -uid "1FB28543-46DB-5AA7-FEC7-5F9298077299";
	setAttr ".t" -type "double3" 2.1461603077446441 2.886579864025407e-15 4.8049016263467711e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -0.47060966426211664 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.7105317517007671;
createNode joint -n "spine_5_bind" -p "spine_4_bind";
	rename -uid "1C85430E-4AF3-4E6A-D2CF-AD82C0DF995D";
	setAttr ".t" -type "double3" 2.1461748457901635 -4.9960036108132044e-16 5.0280327417080819e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.7105317517007671;
createNode joint -n "chest_bind" -p "spine_5_bind";
	rename -uid "77DB40FA-41EC-C5C3-55B6-968C6381BDAA";
	setAttr ".t" -type "double3" 0.98302637098055357 -3.219646771412954e-15 7.072431898025452e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".ds" 1;
	setAttr ".radi" 0.7105317517007671;
createNode joint -n "clavicle_l_bind" -p "chest_bind";
	rename -uid "5FADFC38-485E-E2E0-2999-2EA573B66997";
	setAttr ".t" -type "double3" 3.4563364470394617 0.29097277449107939 -0.50739552666481691 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.5444437451708128e-14 89.999999999999986 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.0963552587732772;
createNode joint -n "shoulder_l_bind" -p "clavicle_l_bind";
	rename -uid "E7E77579-4671-4D4D-9883-0592814235AB";
	setAttr ".t" -type "double3" 4.8621117171044164 0.75927666819435691 -1.4881860579139214 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.0034088890598205383 31.926965677823009 1.0550469018839825 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.6120192782886267;
createNode joint -n "elbow_l_bind" -p "shoulder_l_bind";
	rename -uid "1B4AF053-46B8-94CC-9C81-E0B24C884741";
	setAttr ".t" -type "double3" 9.2302130770416486 1.8041124150158814e-16 -2.131628207280293e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 0.26740854230873118 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".radi" 1.7532977611069911;
createNode joint -n "wrist_l_bind" -p "elbow_l_bind";
	rename -uid "E2AD7265-4AEA-6888-E639-9EA05F16E1FB";
	setAttr ".t" -type "double3" 9.692692549504379 4.7184478546569153e-15 0 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".ds" 1;
	setAttr ".radi" 1.7532977611069911;
createNode joint -n "ring_001_l_bind" -p "wrist_l_bind";
	rename -uid "1A7E0128-4B0B-C9D2-E6C2-75868A5CCF89";
	setAttr ".t" -type "double3" 1.7956864487626198 0.30024764952583727 -0.098184583846816054 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 89.987579230963561 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.70623473334183484;
createNode joint -n "ring_002_l_bind" -p "ring_001_l_bind";
	rename -uid "4D40C737-48B4-EC27-C836-12ACA8709A3F";
	setAttr ".t" -type "double3" 1.7294694339947547 0.077313055209863535 -0.12825489606387042 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.011320797092973501 2.0115687518123009 3.3223604275102043 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.64221869959915556;
createNode joint -n "ring_003_l_bind" -p "ring_002_l_bind";
	rename -uid "0BE8DF9A-4673-DFE5-7A36-2FA6E07CA875";
	setAttr ".t" -type "double3" 1.5847984338885546 7.1054273576010019e-15 -4.7184478546569153e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60305093366767737;
createNode joint -n "ring_004_l_bind" -p "ring_003_l_bind";
	rename -uid "B22BD083-4D4A-6CD0-D26C-ABB7E6835095";
	setAttr ".t" -type "double3" 1.1378854950106572 1.4210854715202004e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61753195703979313;
createNode joint -n "ring_005_l_bind" -p "ring_004_l_bind";
	rename -uid "733F15F7-4F24-CF74-595E-34A90FBD9851";
	setAttr ".t" -type "double3" 1.2443480298222127 -7.1054273576010019e-15 -2.2204460492503131e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61753195703979313;
createNode joint -n "middle_001_l_bind" -p "wrist_l_bind";
	rename -uid "F81AA6D3-48EF-2836-7230-5E8464F53AD1";
	setAttr ".t" -type "double3" 1.890124444755628 -0.25825640038353748 -0.13240714921620622 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90.02532285152148 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.7133058373250355;
createNode joint -n "middle_002_l_bind" -p "middle_001_l_bind";
	rename -uid "DC995E3A-4930-124D-87EA-28A21708A514";
	setAttr ".t" -type "double3" 1.8130842495608341 0.11172795254890389 0.2202046676055345 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.06576461522034549 -2.4193122320420288 1.2351415471373066 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.64667058620916296;
createNode joint -n "middle_003_l_bind" -p "middle_002_l_bind";
	rename -uid "60B69F07-4C65-CB29-2E7D-BD98AE7D1F54";
	setAttr ".t" -type "double3" 1.5776464358356073 7.1054273576010019e-15 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.62908348685191151;
createNode joint -n "middle_004_l_bind" -p "middle_003_l_bind";
	rename -uid "D6DAC452-4486-1CEE-7BD7-4A9AEE41F84D";
	setAttr ".t" -type "double3" 1.3292733222651307 7.1054273576010019e-15 -3.3306690738754696e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61883271203419032;
createNode joint -n "middle_005_l_bind" -p "middle_004_l_bind";
	rename -uid "D5F5F7EB-4214-B9D1-B1E5-D0A3DB7E5D26";
	setAttr ".t" -type "double3" 1.2539110054706661 0 6.6613381477509392e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61883271203419032;
createNode joint -n "index_001_l_bind" -p "wrist_l_bind";
	rename -uid "630A9AF6-4C64-94C2-B3D5-AE9246173959";
	setAttr ".t" -type "double3" 1.7738741102685509 -0.88623599219806581 -0.223915269045321 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90.056502378747112 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.71042194109365497;
createNode joint -n "index_002_l_bind" -p "index_001_l_bind";
	rename -uid "8152F6E2-408C-C603-FA17-5AB75EAE443B";
	setAttr ".t" -type "double3" 1.7535805054668501 0.18034994476651178 0.53307279562037868 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.23429205623831423 -7.6148640096749354 1.2249234992387095 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.63154789641426312;
createNode joint -n "index_003_l_bind" -p "index_002_l_bind";
	rename -uid "95A916E1-42E1-D55A-8F12-C393F3D9F80B";
	setAttr ".t" -type "double3" 1.4343165414138568 1.4210854715202004e-14 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.09823052240551583 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.59730073546413442;
createNode joint -n "index_004_l_bind" -p "index_003_l_bind";
	rename -uid "A58F4BD6-4FA2-7F55-84A3-44A93B8A9385";
	setAttr ".t" -type "double3" 1.0956108117450363 2.1316282072803006e-14 2.2204460492503131e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6054846199577113;
createNode joint -n "index_005_l_bind" -p "index_004_l_bind";
	rename -uid "B6ECF957-40B6-C762-CA68-97B85EF07F89";
	setAttr ".t" -type "double3" 1.1557776290618982 0 4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -9.9785917824258525e-17 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6054846199577113;
createNode joint -n "pinkyCup_l_bind" -p "wrist_l_bind";
	rename -uid "3EE821E6-4B31-4D99-78F0-0DBE1BA9F1B4";
	setAttr ".t" -type "double3" 0.89284403796260037 0.14438980060652318 -0.094601276203597706 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 90 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.58462429399591631;
createNode joint -n "pinky_001_l_bind" -p "pinkyCup_l_bind";
	rename -uid "7B765B1D-406A-EC99-2672-09B5B405F0DA";
	setAttr ".t" -type "double3" 0.018993449081925462 0.67357437642717088 0.77204932844310648 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 89.967637834589027 -89.999999999999986 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.66523462925696331;
createNode joint -n "pinky_002_l_bind" -p "pinky_001_l_bind";
	rename -uid "9242FC6A-4D52-F8E0-05FB-7BA737B33B0B";
	setAttr ".t" -type "double3" 1.563662977116028 0.04697394899680063 -0.31135402058406081 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.20493834479556342 10.812120844704872 -0.98722860380915312 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.55766456389613595;
createNode joint -n "pinky_003_l_bind" -p "pinky_002_l_bind";
	rename -uid "0E9CDAEC-4D63-EE57-9590-DC947219CA47";
	setAttr ".t" -type "double3" 0.8042110130622504 7.1054273576010019e-15 3.5527136788005009e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.58717843113653168;
createNode joint -n "pinky_004_l_bind" -p "pinky_003_l_bind";
	rename -uid "8295397D-4450-CE95-28F7-BBBA2437A172";
	setAttr ".t" -type "double3" 1.0211929927029217 -7.1054273576010019e-15 1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60466921364117221;
createNode joint -n "pinky_005_l_bind" -p "pinky_004_l_bind";
	rename -uid "E5344F91-4610-A9B5-184A-FBA6FD32F712";
	setAttr ".t" -type "double3" 1.1497828715693217 7.1054273576010019e-15 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60466921364117221;
createNode joint -n "thumbCup_l_bind" -p "wrist_l_bind";
	rename -uid "8C473596-4AD5-D4D1-490A-3CB4B25280B9";
	setAttr ".t" -type "double3" 0.84100219788065544 -0.19801137691296511 -0.094601276203590601 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -90 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.56575603516008355;
createNode joint -n "thumb_001_l_bind" -p "thumbCup_l_bind";
	rename -uid "34BA56D6-4ECD-1ED5-418B-E8811935D453";
	setAttr ".t" -type "double3" -0.2582459138893114 -1.1127238754382298 -0.16372551611508257 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 19.084244512636808 25.031521757363706 -108.19973844192134 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.57225036426237008;
createNode joint -n "thumb_002_l_bind" -p "thumb_001_l_bind";
	rename -uid "B4977729-467D-2F92-7E7F-A7AD9E8E10A9";
	setAttr ".t" -type "double3" 0.91144385423249696 -1.4210854715202004e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.6250723404906262 -6.8407145483025102 -14.305906863274279 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61534233056175225;
createNode joint -n "thumb_003_l_bind" -p "thumb_002_l_bind";
	rename -uid "9349A052-4B36-ED7F-A34B-9BB3386E3E88";
	setAttr ".t" -type "double3" 1.2282501906604093 1.0658141036401503e-14 2.8421709430404007e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 4.6052880431250145 0.96200147535731706 12.187701734410735 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6380377139822444;
createNode joint -n "thumb_004_l_bind" -p "thumb_003_l_bind";
	rename -uid "C74ABA52-424D-B231-2095-8B86A7001C07";
	setAttr ".t" -type "double3" 1.3951035949659776 1.0658141036401503e-14 -2.1316282072803006e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6380377139822444;
createNode joint -n "wristTwist_l_bind" -p "wrist_l_bind";
	rename -uid "83268997-416C-5366-AFE6-44A13EA6A52F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 7.1054273576010019e-15 0 0 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -8.9808303459168822e-21 2.1707844107738029e-17 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".ds" 1;
	setAttr ".radi" 1.7532977611069911;
createNode aimConstraint -n "wristTwist_l_bind_aimConstraint1" -p "wristTwist_l_bind";
	rename -uid "A85585C8-49B5-64D5-34C0-5C9E66007AAF";
	addAttr -dcb 0 -ci true -sn "w0" -ln "elbow_l_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".a" -type "double3" -1 0 0 ;
	setAttr ".wut" 4;
	setAttr -k on ".w0";
createNode joint -n "shoulderNoTwist_l_bind" -p "clavicle_l_bind";
	rename -uid "F220B64A-4EA6-75D4-5936-59B7B74B9014";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.6120192782886267;
createNode aimConstraint -n "shoulderNoTwist_l_bind_aimConstraint1" -p "shoulderNoTwist_l_bind";
	rename -uid "AEEF8153-4039-DE70-662B-0F8AA3FDC6E8";
	addAttr -dcb 0 -ci true -sn "w0" -ln "elbow_l_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".wut" 4;
	setAttr ".rsrr" -type "double3" -0.0017045845735772825 1.6061876038436652e-15 8.0236621053579815e-15 ;
	setAttr -k on ".w0";
createNode joint -n "neck_0_bind" -p "chest_bind";
	rename -uid "18D9AFE1-4DB0-791B-FACD-E6B85F8C66DE";
	setAttr ".t" -type "double3" 3.6214886864772353 0.46580246916033191 -0.0089040991555436339 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.6498000615042016e-30 1.2722218725854065e-14 -6.3611093629270367e-15 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.63586082232741115;
createNode joint -n "neck_1_bind" -p "neck_0_bind";
	rename -uid "86375045-4898-12A7-769E-FF9FEE736D36";
	setAttr ".t" -type "double3" 1.5637189323694187 -1.6653345369377348e-16 8.6736173798840355e-18 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.66247185415554244;
createNode joint -n "neck_2_bind" -p "neck_1_bind";
	rename -uid "262C4566-4801-6049-49C7-A49DE91A53E7";
	setAttr ".t" -type "double3" 1.5637189323694187 0 3.9725167599868882e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.63068832643249984;
createNode joint -n "neck_3_bind" -p "neck_2_bind";
	rename -uid "9C4DAFFE-474C-A432-DF38-FF8FD00E3B83";
	setAttr ".t" -type "double3" 1.5637189323694187 -2.7755575615628914e-17 3.4694469519536142e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.65060451186979973;
createNode joint -n "skull_bind" -p "neck_3_bind";
	rename -uid "0DC75A00-4DDF-7D9F-132E-5480F39E1F17";
	setAttr ".t" -type "double3" 1.5637189323694187 2.7755575615628914e-17 3.7643499428696714e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.0310071166499839;
createNode joint -n "eyeSocket_l_bind" -p "skull_bind";
	rename -uid "59EC5218-4975-B946-5808-47A6A1407176";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 3.8024380015218924 -2.1640329093146367 -1.0221053364981405 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90 89.999999999999986 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".bps" -type "matrix" 1 -5.4316870729137587e-17 1.6898918048191827e-16 0
		 5.9147725364742018e-17 1 -1.6653345369377348e-16 0 -1.6405086059206697e-16 1.6653345369377348e-16 1 0
		 1.0310094356536863 62.513282775878906 1.9892032146453857 1;
	setAttr ".radi" 0.5;
createNode joint -n "eye_l_bind" -p "eyeSocket_l_bind";
	rename -uid "AF31F74A-4EA2-2FF2-0DF3-57A0E0CCDBB6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.8249000307521015e-30 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".bps" -type "matrix" 1 -5.4316870729137587e-17 1.6898918048191827e-16 0
		 5.9147725364742018e-17 1 -1.6653345369377348e-16 0 -1.6405086059206697e-16 1.6653345369377348e-16 1 0
		 1.0310094356536863 62.513282775878906 1.9892032146453857 1;
	setAttr ".radi" 0.5;
createNode joint -n "eyeSocket_r_bind" -p "skull_bind";
	rename -uid "2C2D499B-475A-4676-A683-DEA541B31EF4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.8024552256429871 -2.1640296946692512 1.0399140991555464 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90 89.999999999999986 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".bps" -type "matrix" 1 -5.4316870729137587e-17 1.6898918048191827e-16 0
		 5.9147725364742018e-17 1 -1.6653345369377348e-16 0 -1.6405086059206697e-16 1.6653345369377348e-16 1 0
		 -1.0310100000000009 62.513300000000001 1.9892000000000007 1;
	setAttr ".radi" 0.5;
createNode joint -n "eye_r_bind" -p "eyeSocket_r_bind";
	rename -uid "4B687382-40FB-5D8E-E118-60BD5ED4CAF9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0 -2.2204460492503131e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.8249000307521015e-30 0 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".bps" -type "matrix" 1 -5.4316870729137587e-17 1.6898918048191827e-16 0
		 5.9147725364742018e-17 1 -1.6653345369377348e-16 0 -1.6405086059206697e-16 1.6653345369377348e-16 1 0
		 -1.0310100000000009 62.513300000000001 1.9892000000000007 1;
	setAttr ".radi" 0.5;
createNode joint -n "clavicle_r_bind" -p "chest_bind";
	rename -uid "079FD2AC-4ED7-9267-60B9-07BAE2998129";
	setAttr ".t" -type "double3" 3.4563196415978936 0.29097277449107961 0.50739600000000029 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -179.99999999999997 89.999999999999972 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.0963552587732772;
createNode joint -n "shoulder_r_bind" -p "clavicle_r_bind";
	rename -uid "7F6CBBB0-4963-CFFF-ADF0-73B180B629FB";
	setAttr ".t" -type "double3" -4.862114 -0.75927700000000165 1.4881999999999991 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.0034088890624072938 31.926965677822995 1.0550469018839874 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.6120192782886267;
createNode joint -n "elbow_r_bind" -p "shoulder_r_bind";
	rename -uid "32E76E7F-4276-9661-4C74-F7BF05E32F09";
	setAttr ".t" -type "double3" -9.2302417312940683 9.4642726033988822e-07 -1.2535513462808012e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.1222542851065401e-17 9.0943985423161137e-15 0.26740854230891864 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".radi" 1.7532977611069911;
createNode joint -n "wrist_r_bind" -p "elbow_r_bind";
	rename -uid "0D7C1EE3-41AD-5E6D-F732-CA8CB8D05CB3";
	setAttr ".t" -type "double3" -9.6926950098076308 2.9023279760620468e-06 -6.7764683038262774e-06 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".ds" 1;
	setAttr ".radi" 1.7532977611069911;
createNode joint -n "ring_001_r_bind" -p "wrist_r_bind";
	rename -uid "EA902170-4737-6F9D-F91E-828D428C3D3D";
	setAttr ".t" -type "double3" -1.7957012365329332 -0.30025468061592808 0.098185461155360088 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 89.987579230960947 -1.7836461544269843e-13 -1.9650459697040597e-13 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.70623473334183484;
createNode joint -n "ring_002_r_bind" -p "ring_001_r_bind";
	rename -uid "F2C67E33-4E62-B2F3-F413-D9920F1D9297";
	setAttr ".t" -type "double3" -1.7294042636290561 -0.077368687307036055 0.12825110356650105 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.011320797108096711 2.0115687518121006 3.3223604275101715 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.64221869959915556;
createNode joint -n "ring_003_r_bind" -p "ring_002_r_bind";
	rename -uid "3FACD500-4A1B-3406-C42D-ABB1F613DAD3";
	setAttr ".t" -type "double3" -1.5848539933317207 4.3731306170968764e-05 -2.8397816722591784e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60305093366767737;
createNode joint -n "ring_004_r_bind" -p "ring_003_r_bind";
	rename -uid "8C383045-49FC-5EDB-63F1-B6B720921B02";
	setAttr ".t" -type "double3" -1.1378566840495523 -3.1035675768009696e-05 -7.4344131761883148e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61753195703979313;
createNode joint -n "ring_005_r_bind" -p "ring_004_r_bind";
	rename -uid "59CE2D00-432A-D935-DD85-1FB5A6AC52F1";
	setAttr ".t" -type "double3" -1.2443527294946817 3.1152454354810288e-05 5.3545548599487347e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61753195703979313;
createNode joint -n "middle_001_r_bind" -p "wrist_r_bind";
	rename -uid "421212C1-47AD-9DC1-2C15-E2A04324C444";
	setAttr ".t" -type "double3" -1.8900793113280063 0.25825328617160964 0.13233462742375934 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90.025322851518851 -1.7835861264634177e-13 -1.9662808166149973e-13 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.7133058373250355;
createNode joint -n "middle_002_r_bind" -p "middle_001_r_bind";
	rename -uid "5E3BFEC4-4A27-2721-2669-BFB5E75619E2";
	setAttr ".t" -type "double3" -1.813106727368927 -0.11165708330207735 -0.22020470452287444 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.065764615196772652 -2.4193122320421994 1.2351415471372844 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.64667058620916296;
createNode joint -n "middle_003_r_bind" -p "middle_002_r_bind";
	rename -uid "65D777FC-4836-99BF-4258-EB9B5E4F6008";
	setAttr ".t" -type "double3" -1.577596209812868 -2.9606822664618448e-06 -5.6658841646184399e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159366e-07 1.4317695989370061e-22 2.7843950428346754e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.62908348685191151;
createNode joint -n "middle_004_r_bind" -p "middle_003_r_bind";
	rename -uid "5832FDB1-4786-4A8C-4A8F-39A2078FFBE0";
	setAttr ".t" -type "double3" -1.3292733032103636 -4.3771051608132439e-05 -5.481901119153143e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159366e-07 1.4317695989370061e-22 2.7843950428346754e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61883271203419032;
createNode joint -n "middle_005_r_bind" -p "middle_004_r_bind";
	rename -uid "F8E7337C-465A-4F54-95D0-039E753102C9";
	setAttr ".t" -type "double3" -1.2539322000899702 -8.7918541780140913e-06 4.8029520993697616e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159366e-07 1.4317695989370061e-22 2.7843950428346754e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61883271203419032;
createNode joint -n "index_001_r_bind" -p "wrist_r_bind";
	rename -uid "CD95B164-4962-1119-66C5-DF86CF6AA930";
	setAttr ".t" -type "double3" -1.7738374734052744 0.88623313953187788 0.22387300869609561 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90.056502378744497 -1.783535924578937e-13 -1.9673008780143363e-13 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.71042194109365497;
createNode joint -n "index_002_r_bind" -p "index_001_r_bind";
	rename -uid "3E90D796-41F4-4E3A-F7E5-C99A79FD46B4";
	setAttr ".t" -type "double3" -1.7536120943279569 -0.1803359246691727 -0.53307273222742102 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.23429205624156868 -7.6148640096751024 1.2249234992386977 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.63154789641426312;
createNode joint -n "index_003_r_bind" -p "index_002_r_bind";
	rename -uid "19770C9E-45D5-F889-1907-1B843965031B";
	setAttr ".t" -type "double3" -1.4343156422860801 6.0960137489018962e-06 -5.4623054845936991e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.09823052241217628 -1.8892483902937561e-17 2.9974703888304185e-17 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.59730073546413442;
createNode joint -n "index_004_r_bind" -p "index_003_r_bind";
	rename -uid "8CD42036-471E-0A26-EDCB-B380DEAB33C4";
	setAttr ".t" -type "double3" -1.0955551904960226 -1.0429255787869351e-05 -6.1193276365001381e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159387e-07 -1.6532345697704393e-22 2.6066676773708483e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6054846199577113;
createNode joint -n "index_005_r_bind" -p "index_004_r_bind";
	rename -uid "2CCB299B-4828-1FF3-E3F6-D1AFAA3E4B83";
	setAttr ".t" -type "double3" -1.1557885892839863 -2.1172416737158528e-05 1.2993285183338088e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159387e-07 -1.6532345697704393e-22 2.6066676773708483e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6054846199577113;
createNode joint -n "pinkyCup_r_bind" -p "wrist_r_bind";
	rename -uid "7ABDE688-4033-1133-D1FA-C2B566073685";
	setAttr ".t" -type "double3" -0.8928339734591213 -0.14439329311297999 0.094618213580524468 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.625547889548133e-12 89.999999999997385 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.58462429399591631;
createNode joint -n "pinky_001_r_bind" -p "pinkyCup_r_bind";
	rename -uid "CB288696-423D-0BC1-18EA-E59F23CDE46E";
	setAttr ".t" -type "double3" -0.018976040280399786 -0.67357590251648658 -0.77206226144293222 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 89.967637834586398 -89.999999999997385 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.66523462925696331;
createNode joint -n "pinky_002_r_bind" -p "pinky_001_r_bind";
	rename -uid "79329C71-4B15-2A07-712C-B3B2E0572D00";
	setAttr ".t" -type "double3" -1.5636307484490475 -0.046967889489259562 0.31135749543188584 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.20493834479845116 10.81212084470468 -0.98722860380916011 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.55766456389613595;
createNode joint -n "pinky_003_r_bind" -p "pinky_002_r_bind";
	rename -uid "F6AD7E4C-4C0A-0BBD-F6A1-C48C4ED733FE";
	setAttr ".t" -type "double3" -0.80416893998682637 -1.0220116095638332e-06 7.7081428864200774e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 1.8222470526871276e-22 -2.0107553259033724e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.58717843113653168;
createNode joint -n "pinky_004_r_bind" -p "pinky_003_r_bind";
	rename -uid "4F1EFF58-4369-8C46-4E74-26BFD5E52F56";
	setAttr ".t" -type "double3" -1.0211797409791199 -5.2085164824688945e-05 9.8199842413215777e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 1.8222470526871276e-22 -2.0107553259033724e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60466921364117221;
createNode joint -n "pinky_005_r_bind" -p "pinky_004_r_bind";
	rename -uid "A7F7A6FF-41E6-1493-78AC-14A5BC88C649";
	setAttr ".t" -type "double3" -1.1498660115253927 2.2765280576209079e-05 -2.4908146172730738e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 1.8222470526871276e-22 -2.0107553259033724e-22 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.60466921364117221;
createNode joint -n "thumbCup_r_bind" -p "wrist_r_bind";
	rename -uid "D7943AD2-4AB3-BEAE-2062-E2A8704C2936";
	setAttr ".t" -type "double3" -0.84091403628401462 0.19800667296640373 0.094611766130263675 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.6254484972143362e-12 -89.999999999997385 0 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.56575603516008355;
createNode joint -n "thumb_001_r_bind" -p "thumbCup_r_bind";
	rename -uid "CFE18658-4AEC-8099-FB34-8185C74DEDF1";
	setAttr ".t" -type "double3" 0.25823928298343191 1.1127251915955778 0.16380223403176508 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 19.084244512639607 25.031521757364331 -108.19973844191755 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.57225036426237008;
createNode joint -n "thumb_002_r_bind" -p "thumb_001_r_bind";
	rename -uid "31584BF2-4E59-C83C-AEC6-49A7570A8B58";
	setAttr ".t" -type "double3" -0.91141490885950205 -1.6464026664664289e-05 -6.0519076818366102e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.6250723404906564 -6.8407145483024934 -14.30590686327424 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.61534233056175225;
createNode joint -n "thumb_003_r_bind" -p "thumb_002_r_bind";
	rename -uid "283437E4-4DC8-AB48-E85E-FC87848AB1DE";
	setAttr ".t" -type "double3" -1.228275406349205 2.2069958525605671e-05 1.5218629108915138e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 4.6052880431249763 0.96200147535731617 12.187701734410727 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6380377139822444;
createNode joint -n "thumb_004_r_bind" -p "thumb_003_r_bind";
	rename -uid "A25D8D05-4CBF-63BF-BF7F-6F9F25D611B1";
	setAttr ".t" -type "double3" -1.3950956024896577 -1.5129952494419285e-05 4.6744919579566613e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 0.6380377139822444;
createNode joint -n "wristTwist_r_bind" -p "wrist_r_bind";
	rename -uid "D1B7F752-4070-B9DB-AE22-5F9A74A696BF";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1.7763568394002505e-15 -2.2204460492503131e-16 -7.1054273576010019e-15 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".ds" 1;
	setAttr ".radi" 1.7532977611069911;
createNode aimConstraint -n "wristTwist_l_bind_aimConstraint2" -p "wristTwist_r_bind";
	rename -uid "2FEFA974-42F8-C936-C275-9CA4786CFC14";
	addAttr -dcb 0 -ci true -sn "w0" -ln "elbow_l_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t" -type "double3" 1.7763568394002505e-15 0 0 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tt" -type "double3" 9.2302130770416486 1.8041124150158814e-16 -2.131628207280293e-14 ;
	setAttr ".tg[0].tpm" -type "matrix" 0.8485790023497819 -0.52883783610134882 -0.015627535912350988 0
		 -0.018381542975955106 5.0495903810169308e-05 -0.99983104389091004 0 0.52874927484477174 0.84872288796627049 -0.0096780056479300585 0
		 5.3695072437692337 50.802630747527644 -0.75927666819435657 1;
	setAttr ".cpim" -type "matrix" 0.84848397105062112 -0.022341781963320713 0.52874927484477174 0
		 -0.52883184076742373 0.0025186569300903912 0.8487228879662706 0 -0.020293719735590344 -0.9997472186237738 -0.009678005647930062 0
		 3.3718942586244443 -0.72399605474144291 -45.963826829625553 1;
	setAttr ".a" -type "double3" -1 0 0 ;
	setAttr ".wut" 4;
	setAttr ".ct" -type "double3" 7.1054273576010019e-15 0 0 ;
	setAttr ".cro" 1;
	setAttr ".cjo" -type "double3" -8.9808303459168822e-21 2.1707844107738029e-17 0 ;
	setAttr -k on ".w0";
createNode joint -n "shoulderNoTwist_r_bind" -p "clavicle_r_bind";
	rename -uid "92BC361F-4959-8CAB-733D-2A92CDC5B352";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -4.862114 -0.75927700000000165 1.4881999999999991 ;
	setAttr ".r" -type "double3" 0.29840118737066157 1.3706806687410463e-13 1.1396490382030716e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.0034088890624072938 31.926965677822995 1.0550469018839874 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 1.6120192782886267;
createNode aimConstraint -n "shoulderNoTwist_l_bind_aimConstraint2" -p "shoulderNoTwist_r_bind";
	rename -uid "2DE1828B-4F7F-25F6-D3EA-B094501E6F8E";
	addAttr -dcb 0 -ci true -sn "w0" -ln "elbow_l_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t" -type "double3" 0 -1.1102230246251565e-16 0 ;
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tt" -type "double3" 9.2302130770416486 1.8041124150158814e-16 -2.131628207280293e-14 ;
	setAttr ".tg[0].tpm" -type "matrix" 0.8485790023497819 -0.52883783610134882 -0.015627535912350988 0
		 -0.018381542975955106 5.0495903810169308e-05 -0.99983104389091004 0 0.52874927484477174 0.84872288796627049 -0.0096780056479300585 0
		 5.3695072437692337 50.802630747527644 -0.75927666819435657 1;
	setAttr ".cpim" -type "matrix" 1 -2.2204460492503131e-16 0 0 1.0947644252537633e-47 4.9303806576313238e-32 1 0
		 -2.2204460492503131e-16 -1 0 0 -0.50739552666481713 1.5559543712717185e-15 -52.290816805441565 1;
	setAttr ".wut" 4;
	setAttr ".ct" -type "double3" 4.8621117171044164 0.75927666819435691 -1.4881860579139214 ;
	setAttr ".cjo" -type "double3" 0.0034088890598205383 31.926965677823009 1.0550469018839825 ;
	setAttr ".rsrr" -type "double3" -0.0017045845735772825 1.6061876038436652e-15 8.0236621053579815e-15 ;
	setAttr -k on ".w0";
createNode joint -n "pelvis_l_bind" -p "hips_bind";
	rename -uid "751D0ABC-4C35-574A-4050-738A7A0A02DF";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.6498000615042016e-30 3.8166656177562201e-14 180 ;
	setAttr ".radi" 0.5;
createNode joint -n "thigh_l_bind" -p "pelvis_l_bind";
	rename -uid "92BA6CEE-4A3B-0BA9-E492-F39C4E4C2075";
	setAttr ".t" -type "double3" 2.132095570883962 0.0092199922293613179 -2.070959353991582 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.9625464517308657e-16 -2.5442712717379433e-14 0.66712122832906251 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 2;
createNode joint -n "knee_l_bind" -p "thigh_l_bind";
	rename -uid "2A40DDB6-4E40-C94B-B071-E289E979C3C0";
	setAttr ".t" -type "double3" 16.622397795517948 -2.4424906541753444e-15 -3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" 0 0 -0.28662343434308701 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -3.2079145809397445 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".radi" 2;
createNode joint -n "ankle_l_bind" -p "knee_l_bind";
	rename -uid "94B6B4E4-4E98-5564-207C-E094B98703B8";
	setAttr ".t" -type "double3" 18.215591271511535 -1.0658141036401503e-14 -3.1086244689504383e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.1799079060902519e-15 1.8972232596841195e-14 2.5407933526106983 ;
	setAttr ".radi" 1.1152257881295582;
createNode joint -n "ball_l_bind" -p "ankle_l_bind";
	rename -uid "2F2AA127-4711-1F03-4D03-2AB4652F5390";
	setAttr ".t" -type "double3" 1.4601874263775287 4.6808609712069877 -1.3322676295501878e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.1109549193990954e-16 3.498545472072542e-14 0 ;
	setAttr ".radi" 0.83630727057387044;
createNode joint -n "toe_l_bind" -p "ball_l_bind";
	rename -uid "A9E769B2-46AD-FDA8-00E8-71920A01740F";
	setAttr ".t" -type "double3" -3.3306690738754696e-16 2.8527546896638496 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.83630727057387044;
createNode joint -n "ankleTwist_l_bind" -p "ankle_l_bind";
	rename -uid "AA46408B-4D02-AD1F-68AA-118EFFD13028";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.9968028886505635e-15 -1.1102230246251565e-16 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -5.5725567012883252e-30 -2.4848083448933725e-16 ;
	setAttr ".radi" 1.1152257881295582;
createNode aimConstraint -n "ankleTwist_l_bind_aimConstraint1" -p "ankleTwist_l_bind";
	rename -uid "C8789117-43D6-7E50-E441-4AA01C90C14E";
	addAttr -dcb 0 -ci true -sn "w0" -ln "knee_l_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".a" -type "double3" -1 0 0 ;
	setAttr ".wut" 4;
	setAttr ".rsrr" -type "double3" -2.4781492694166962e-16 1.1174795074152342e-14 -2.5407933526106632 ;
	setAttr -k on ".w0";
createNode joint -n "thighNoTwist_l_bind" -p "pelvis_l_bind";
	rename -uid "DCBA3D57-46BE-3EDC-6937-BA9D03C9B5EB";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 2;
createNode aimConstraint -n "thighNoTwist_l_bind_aimConstraint1" -p "thighNoTwist_l_bind";
	rename -uid "8BDDFC1A-4061-1D5C-C907-F19277C7303C";
	addAttr -dcb 0 -ci true -sn "w0" -ln "knee_l_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".wut" 4;
	setAttr ".rsrr" -type "double3" 7.1292888034567654e-17 1.2245856591667061e-14 -3.6745345804283183e-13 ;
	setAttr -k on ".w0";
createNode joint -n "pelvis_r_bind" -p "hips_bind";
	rename -uid "333FA992-42FA-AAE7-F4D0-2EB89EF6902D";
	setAttr ".t" -type "double3" 0.00010539229455019949 8.6414531363931957e-08 4.6774798987453337e-20 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.5;
createNode joint -n "thigh_r_bind" -p "pelvis_r_bind";
	rename -uid "6128F159-46A9-29C8-62F6-7A804CCF3547";
	setAttr ".t" -type "double3" -2.1322057517038502 -0.0092199997602691597 2.0709596425976411 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.9365750262702083e-16 -5.0441043466971936e-14 0.66712122832869514 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 2;
createNode joint -n "knee_r_bind" -p "thigh_r_bind";
	rename -uid "8E5C7171-4A8F-BE08-8101-259FDD3E3C5B";
	setAttr ".t" -type "double3" -16.622376171710332 -9.8616752519653517e-07 -6.6613381477509392e-15 ;
	setAttr ".r" -type "double3" 0 0 -0.28662343434308701 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364772254292e-07 -5.2530800091273976e-14 -3.207914580939403 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".radi" 2;
createNode joint -n "ankle_r_bind" -p "knee_r_bind";
	rename -uid "4CC0E0E1-4EFE-4BD1-B81F-38AB588C479F";
	setAttr ".t" -type "double3" -18.215607948829298 -5.7400237174487501e-07 -7.9936057773011271e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.1327438162239398e-15 -5.1079166917153752e-14 2.5407933526106636 ;
	setAttr ".radi" 1.1152257881295582;
createNode joint -n "ball_r_bind" -p "ankle_r_bind";
	rename -uid "6BFEE517-44ED-DDE7-DF1F-6A806428CAF9";
	setAttr ".t" -type "double3" -1.4601871874969516 -4.6808527343479094 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.83630727057387044;
createNode joint -n "toe_r_bind" -p "ball_r_bind";
	rename -uid "25287AED-4F9F-375A-7FE5-B4ACA3F52103";
	setAttr ".t" -type "double3" -4.8001935271102525e-07 -2.8527749622789749 1.3322676295501878e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.83630727057387044;
createNode joint -n "ankleTwist_r_bind" -p "ankle_r_bind";
	rename -uid "2B6AB1CA-46D3-AEDC-48C8-94BE048474D5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1.7763568394002505e-15 -2.2204460492503131e-16 -1.3322676295501878e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 1.1152257881295582;
createNode aimConstraint -n "ankleTwist_r_bind_aimConstraint1" -p "ankleTwist_r_bind";
	rename -uid "51A1236E-4D7B-D85A-FD43-3BAAF668C2BB";
	addAttr -dcb 0 -ci true -sn "w0" -ln "knee_r_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".wut" 4;
	setAttr ".rsrr" -type "double3" 6.1953630975088914e-16 -2.7936962107643037e-14 -2.5407915471306159 ;
	setAttr -k on ".w0";
createNode joint -n "thighNoTwist_r_bind" -p "pelvis_r_bind";
	rename -uid "11A67E95-4552-4263-8815-119A3CED21C8";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".jox";
	setAttr -k on ".joy";
	setAttr -k on ".joz";
	setAttr ".radi" 2;
createNode aimConstraint -n "thighNoTwist_r_bind_aimConstraint1" -p "thighNoTwist_r_bind";
	rename -uid "50E3B6CC-48F4-0B56-026C-9F89AA73C046";
	addAttr -dcb 0 -ci true -sn "w0" -ln "knee_r_bindW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".a" -type "double3" -1 0 0 ;
	setAttr ".wut" 4;
	setAttr ".rsrr" -type "double3" -3.9439532143208e-12 2.2961010978978941e-14 -179.99999660077302 ;
	setAttr -k on ".w0";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "DCC8B672-4793-FF6B-4BD2-A0BEB6668A1B";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "EFF71790-4DB3-E21F-7EC3-3BAD1B4DB22B";
	setAttr -s 5 ".bsdt";
	setAttr ".bsdt[0].bscd" -type "Int32Array" 1 -1 ;
	setAttr ".bsdt[1].bscd" -type "Int32Array" 1 -2 ;
	setAttr ".bsdt[1].bsdn" -type "string" "skeleton";
	setAttr ".bsdt[2].bscd" -type "Int32Array" 1 -3 ;
	setAttr ".bsdt[2].bspi" 1;
	setAttr ".bsdt[2].bsdn" -type "string" "skeleton";
	setAttr ".bsdt[3].bscd" -type "Int32Array" 1 -4 ;
	setAttr ".bsdt[3].bspi" 2;
	setAttr ".bsdt[3].bsdn" -type "string" "skeleton";
	setAttr ".bsdt[4].bscd" -type "Int32Array" 0 ;
	setAttr ".bsdt[4].bspi" 3;
	setAttr ".bsdt[4].bsdn" -type "string" "biped_model";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "FAAD0198-4964-2975-0D4B-F4BAD653B68E";
createNode displayLayerManager -n "layerManager";
	rename -uid "4497D3CA-4BEC-5811-FC87-2D8A47C14B38";
	setAttr ".cdl" 1;
	setAttr -s 2 ".dli[1]"  1;
createNode displayLayer -n "defaultLayer";
	rename -uid "B245C46F-47E6-D0E9-5B46-8CA40E355519";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "783A319B-49BF-CA85-F9DB-59AAEC306F78";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "DC2A767A-4297-3C22-D975-238C25A8D8E9";
	setAttr ".g" yes;
createNode renderLayerManager -n "skeleton_renderLayerManager";
	rename -uid "F0652E0A-4581-3748-EFF3-9EAFCB082D0C";
createNode renderLayer -n "skeleton_defaultRenderLayer";
	rename -uid "4B0A486A-48F5-B452-C2B7-3B99918C8374";
	setAttr ".g" yes;
createNode renderLayerManager -n "skeleton_skeleton_renderLayerManager";
	rename -uid "FC112AEC-45BB-E3C4-0EC6-D1A548FFC1A3";
createNode renderLayer -n "skeleton_skeleton_defaultRenderLayer";
	rename -uid "1CF833C7-45BD-6794-F163-59A77DD13625";
	setAttr ".g" yes;
createNode renderLayerManager -n "skeleton_skeleton_skeleton_renderLayerManager";
	rename -uid "07704B8D-42FC-0F6A-1B6F-A9AF11C8CB89";
createNode renderLayer -n "skeleton_skeleton_skeleton_defaultRenderLayer";
	rename -uid "660659C9-4189-D656-888A-D9B199FDF4FD";
	setAttr ".g" yes;
createNode renderLayerManager -n "skeleton_skeleton_skeleton_skeleton_renderLayerManager";
	rename -uid "6A489968-42F8-92B9-E847-0D9389B212B6";
createNode renderLayer -n "skeleton_skeleton_skeleton_skeleton_defaultRenderLayer";
	rename -uid "28EB9392-4BD3-F7E5-9758-EDB3DBF9B7FA";
	setAttr ".g" yes;
createNode renderLayerManager -n "biped_model_renderLayerManager";
	rename -uid "577F645D-4979-A241-D5E2-65A2DE5A22B3";
createNode renderLayer -n "biped_model_defaultRenderLayer";
	rename -uid "C6B15543-4B3C-617E-E279-FA992F489274";
	setAttr ".g" yes;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "47A2AF77-4508-6DA0-4223-9AA7080088E8";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -622.61902287839052 -301.19046422224244 ;
	setAttr ".tgi[0].vh" -type "double2" 601.19045230131405 314.28570179712256 ;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "00EE88EF-4C13-79A9-0FFE-258A3DF1B676";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -330.95236780151544 -323.80951094248991 ;
	setAttr ".tgi[0].vh" -type "double2" 317.85713022663526 338.09522466054096 ;
createNode renderLayerManager -n "skeleton_renderLayerManager1";
	rename -uid "9E7AA3DD-4357-F378-89EE-DCB9D114CB92";
createNode renderLayer -n "skeleton_defaultRenderLayer1";
	rename -uid "DE361AB1-4D81-C2A6-2F81-D49795FF5879";
	setAttr ".g" yes;
createNode renderLayerManager -n "skeleton_skeleton_skeleton_skeleton_skeleton_renderLayerManager";
	rename -uid "5450F919-477F-6EC1-7C4C-0AAF932B6363";
createNode renderLayer -n "skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer";
	rename -uid "60C00DDB-447C-B5E3-05C4-2B9A77053938";
	setAttr ".g" yes;
createNode renderLayerManager -n "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_renderLayerManager";
	rename -uid "D35E275F-4DB6-A303-22D4-75A891197AA1";
createNode renderLayer -n "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer";
	rename -uid "2B9A6CD7-4E1F-6AAC-CF68-329CBE583B48";
	setAttr ".g" yes;
createNode renderLayerManager -n "blink_curves_renderLayerManager";
	rename -uid "DF78CAD9-4160-FC8F-4B8F-69B4DB8EC236";
createNode renderLayer -n "blink_curves_defaultRenderLayer";
	rename -uid "3A24C278-4359-AB48-F17E-F99D9ABB52F3";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "92BBB4D6-48D6-B487-C818-14BA3B291A15";
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
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 2509\n            -height 698\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n"
		+ "            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n"
		+ "            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n"
		+ "                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n"
		+ "                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n"
		+ "                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n"
		+ "                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit 2\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n"
		+ "                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n"
		+ "                -traversalDepthLimit 2\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n"
		+ "                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n"
		+ "                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n"
		+ "                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2509\\n    -height 698\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2509\\n    -height 698\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "B1E03083-48D0-E501-AC0D-72AA08CA9665";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo1";
	rename -uid "321B3CDA-41CF-DA99-62B0-EE81FF2EC26E";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 0 -17.460316766506807 ;
	setAttr ".tgi[0].vh" -type "double2" 73.015870114483008 0 ;
	setAttr -s 132 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 2615.71435546875;
	setAttr ".tgi[0].ni[0].y" 2445.71435546875;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1572.857177734375;
	setAttr ".tgi[0].ni[1].y" 1747.142822265625;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" -55.714286804199219;
	setAttr ".tgi[0].ni[2].y" 22.857143402099609;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 1880;
	setAttr ".tgi[0].ni[3].y" 2040;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 2270;
	setAttr ".tgi[0].ni[4].y" 2040;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 2270;
	setAttr ".tgi[0].ni[5].y" 2445.71435546875;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 1572.857177734375;
	setAttr ".tgi[0].ni[6].y" 2344.28564453125;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 2615.71435546875;
	setAttr ".tgi[0].ni[7].y" 2344.28564453125;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 2270;
	setAttr ".tgi[0].ni[8].y" 2141.428466796875;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 958.5714111328125;
	setAttr ".tgi[0].ni[9].y" 1787.142822265625;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 1880;
	setAttr ".tgi[0].ni[10].y" 1621.4285888671875;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 1880;
	setAttr ".tgi[0].ni[11].y" 2445.71435546875;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 651.4285888671875;
	setAttr ".tgi[0].ni[12].y" 1462.857177734375;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 2615.71435546875;
	setAttr ".tgi[0].ni[13].y" 2242.857177734375;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" 1572.857177734375;
	setAttr ".tgi[0].ni[14].y" 2445.71435546875;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[15].y" 1021.4285888671875;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" 1572.857177734375;
	setAttr ".tgi[0].ni[16].y" 2040;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 2270;
	setAttr ".tgi[0].ni[17].y" 2242.857177734375;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 2270;
	setAttr ".tgi[0].ni[18].y" 2344.28564453125;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" 1572.857177734375;
	setAttr ".tgi[0].ni[19].y" 2242.857177734375;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[20].y" 2141.428466796875;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" 2615.71435546875;
	setAttr ".tgi[0].ni[21].y" 2141.428466796875;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[22].y" 2445.71435546875;
	setAttr ".tgi[0].ni[22].nvs" 18304;
	setAttr ".tgi[0].ni[23].x" 1572.857177734375;
	setAttr ".tgi[0].ni[23].y" 2141.428466796875;
	setAttr ".tgi[0].ni[23].nvs" 18304;
	setAttr ".tgi[0].ni[24].x" 1880;
	setAttr ".tgi[0].ni[24].y" 2141.428466796875;
	setAttr ".tgi[0].ni[24].nvs" 18304;
	setAttr ".tgi[0].ni[25].x" 1880;
	setAttr ".tgi[0].ni[25].y" 1938.5714111328125;
	setAttr ".tgi[0].ni[25].nvs" 18304;
	setAttr ".tgi[0].ni[26].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[26].y" 1767.142822265625;
	setAttr ".tgi[0].ni[26].nvs" 18304;
	setAttr ".tgi[0].ni[27].x" 1880;
	setAttr ".tgi[0].ni[27].y" 2344.28564453125;
	setAttr ".tgi[0].ni[27].nvs" 18304;
	setAttr ".tgi[0].ni[28].x" 2615.71435546875;
	setAttr ".tgi[0].ni[28].y" 2040;
	setAttr ".tgi[0].ni[28].nvs" 18304;
	setAttr ".tgi[0].ni[29].x" 651.4285888671875;
	setAttr ".tgi[0].ni[29].y" 1715.7142333984375;
	setAttr ".tgi[0].ni[29].nvs" 18304;
	setAttr ".tgi[0].ni[30].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[30].y" 2344.28564453125;
	setAttr ".tgi[0].ni[30].nvs" 18304;
	setAttr ".tgi[0].ni[31].x" 958.5714111328125;
	setAttr ".tgi[0].ni[31].y" 2174.28564453125;
	setAttr ".tgi[0].ni[31].nvs" 18304;
	setAttr ".tgi[0].ni[32].x" 1880;
	setAttr ".tgi[0].ni[32].y" 1722.857177734375;
	setAttr ".tgi[0].ni[32].nvs" 18304;
	setAttr ".tgi[0].ni[33].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[33].y" 2242.857177734375;
	setAttr ".tgi[0].ni[33].nvs" 18304;
	setAttr ".tgi[0].ni[34].x" 1880;
	setAttr ".tgi[0].ni[34].y" 2242.857177734375;
	setAttr ".tgi[0].ni[34].nvs" 18304;
	setAttr ".tgi[0].ni[35].x" 2270;
	setAttr ".tgi[0].ni[35].y" 1817.142822265625;
	setAttr ".tgi[0].ni[35].nvs" 18304;
	setAttr ".tgi[0].ni[36].x" 2270;
	setAttr ".tgi[0].ni[36].y" 1918.5714111328125;
	setAttr ".tgi[0].ni[36].nvs" 18304;
	setAttr ".tgi[0].ni[37].x" 1880;
	setAttr ".tgi[0].ni[37].y" 1317.142822265625;
	setAttr ".tgi[0].ni[37].nvs" 18304;
	setAttr ".tgi[0].ni[38].x" 2270;
	setAttr ".tgi[0].ni[38].y" 1302.857177734375;
	setAttr ".tgi[0].ni[38].nvs" 18304;
	setAttr ".tgi[0].ni[39].x" 37.142856597900391;
	setAttr ".tgi[0].ni[39].y" 1451.4285888671875;
	setAttr ".tgi[0].ni[39].nvs" 18304;
	setAttr ".tgi[0].ni[40].x" 2270;
	setAttr ".tgi[0].ni[40].y" 1614.2857666015625;
	setAttr ".tgi[0].ni[40].nvs" 18304;
	setAttr ".tgi[0].ni[41].x" 2615.71435546875;
	setAttr ".tgi[0].ni[41].y" 1918.5714111328125;
	setAttr ".tgi[0].ni[41].nvs" 18304;
	setAttr ".tgi[0].ni[42].x" 344.28570556640625;
	setAttr ".tgi[0].ni[42].y" 1454.2857666015625;
	setAttr ".tgi[0].ni[42].nvs" 18304;
	setAttr ".tgi[0].ni[43].x" 1572.857177734375;
	setAttr ".tgi[0].ni[43].y" 1645.7142333984375;
	setAttr ".tgi[0].ni[43].nvs" 18304;
	setAttr ".tgi[0].ni[44].x" -270;
	setAttr ".tgi[0].ni[44].y" 1394.2857666015625;
	setAttr ".tgi[0].ni[44].nvs" 18304;
	setAttr ".tgi[0].ni[45].x" 2270;
	setAttr ".tgi[0].ni[45].y" 1715.7142333984375;
	setAttr ".tgi[0].ni[45].nvs" 18304;
	setAttr ".tgi[0].ni[46].x" 2615.71435546875;
	setAttr ".tgi[0].ni[46].y" 1715.7142333984375;
	setAttr ".tgi[0].ni[46].nvs" 18304;
	setAttr ".tgi[0].ni[47].x" 2615.71435546875;
	setAttr ".tgi[0].ni[47].y" 1614.2857666015625;
	setAttr ".tgi[0].ni[47].nvs" 18304;
	setAttr ".tgi[0].ni[48].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[48].y" 1665.7142333984375;
	setAttr ".tgi[0].ni[48].nvs" 18304;
	setAttr ".tgi[0].ni[49].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[49].y" 1564.2857666015625;
	setAttr ".tgi[0].ni[49].nvs" 18304;
	setAttr ".tgi[0].ni[50].x" 1572.857177734375;
	setAttr ".tgi[0].ni[50].y" 1544.2857666015625;
	setAttr ".tgi[0].ni[50].nvs" 18304;
	setAttr ".tgi[0].ni[51].x" 1880;
	setAttr ".tgi[0].ni[51].y" 1520;
	setAttr ".tgi[0].ni[51].nvs" 18304;
	setAttr ".tgi[0].ni[52].x" 2270;
	setAttr ".tgi[0].ni[52].y" 1512.857177734375;
	setAttr ".tgi[0].ni[52].nvs" 18304;
	setAttr ".tgi[0].ni[53].x" 2615.71435546875;
	setAttr ".tgi[0].ni[53].y" 1512.857177734375;
	setAttr ".tgi[0].ni[53].nvs" 18304;
	setAttr ".tgi[0].ni[54].x" 2545.71435546875;
	setAttr ".tgi[0].ni[54].y" -1230;
	setAttr ".tgi[0].ni[54].nvs" 18304;
	setAttr ".tgi[0].ni[55].x" 2615.71435546875;
	setAttr ".tgi[0].ni[55].y" 1411.4285888671875;
	setAttr ".tgi[0].ni[55].nvs" 18304;
	setAttr ".tgi[0].ni[56].x" 2270;
	setAttr ".tgi[0].ni[56].y" 941.4285888671875;
	setAttr ".tgi[0].ni[56].nvs" 18304;
	setAttr ".tgi[0].ni[57].x" 1880;
	setAttr ".tgi[0].ni[57].y" 647.14288330078125;
	setAttr ".tgi[0].ni[57].nvs" 18304;
	setAttr ".tgi[0].ni[58].x" 1572.857177734375;
	setAttr ".tgi[0].ni[58].y" 261.42855834960938;
	setAttr ".tgi[0].ni[58].nvs" 18304;
	setAttr ".tgi[0].ni[59].x" 2601.428466796875;
	setAttr ".tgi[0].ni[59].y" -1880;
	setAttr ".tgi[0].ni[59].nvs" 18304;
	setAttr ".tgi[0].ni[60].x" 2434.28564453125;
	setAttr ".tgi[0].ni[60].y" -840;
	setAttr ".tgi[0].ni[60].nvs" 18304;
	setAttr ".tgi[0].ni[61].x" 2615.71435546875;
	setAttr ".tgi[0].ni[61].y" 1225.7142333984375;
	setAttr ".tgi[0].ni[61].nvs" 18304;
	setAttr ".tgi[0].ni[62].x" 1572.857177734375;
	setAttr ".tgi[0].ni[62].y" 1067.142822265625;
	setAttr ".tgi[0].ni[62].nvs" 18304;
	setAttr ".tgi[0].ni[63].x" 2584.28564453125;
	setAttr ".tgi[0].ni[63].y" -1620;
	setAttr ".tgi[0].ni[63].nvs" 18304;
	setAttr ".tgi[0].ni[64].x" 958.5714111328125;
	setAttr ".tgi[0].ni[64].y" 1275.7142333984375;
	setAttr ".tgi[0].ni[64].nvs" 18304;
	setAttr ".tgi[0].ni[65].x" 2270;
	setAttr ".tgi[0].ni[65].y" 840;
	setAttr ".tgi[0].ni[65].nvs" 18304;
	setAttr ".tgi[0].ni[66].x" 2270;
	setAttr ".tgi[0].ni[66].y" 1411.4285888671875;
	setAttr ".tgi[0].ni[66].nvs" 18304;
	setAttr ".tgi[0].ni[67].x" 1880;
	setAttr ".tgi[0].ni[67].y" 1418.5714111328125;
	setAttr ".tgi[0].ni[67].nvs" 18304;
	setAttr ".tgi[0].ni[68].x" 2615.71435546875;
	setAttr ".tgi[0].ni[68].y" 1124.2857666015625;
	setAttr ".tgi[0].ni[68].nvs" 18304;
	setAttr ".tgi[0].ni[69].x" 2615.71435546875;
	setAttr ".tgi[0].ni[69].y" 1022.8571166992188;
	setAttr ".tgi[0].ni[69].nvs" 18304;
	setAttr ".tgi[0].ni[70].x" 1572.857177734375;
	setAttr ".tgi[0].ni[70].y" 1442.857177734375;
	setAttr ".tgi[0].ni[70].nvs" 18304;
	setAttr ".tgi[0].ni[71].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[71].y" 728.5714111328125;
	setAttr ".tgi[0].ni[71].nvs" 18304;
	setAttr ".tgi[0].ni[72].x" 1572.857177734375;
	setAttr ".tgi[0].ni[72].y" 864.28570556640625;
	setAttr ".tgi[0].ni[72].nvs" 18304;
	setAttr ".tgi[0].ni[73].x" 1880;
	setAttr ".tgi[0].ni[73].y" 860;
	setAttr ".tgi[0].ni[73].nvs" 18304;
	setAttr ".tgi[0].ni[74].x" 1880;
	setAttr ".tgi[0].ni[74].y" 961.4285888671875;
	setAttr ".tgi[0].ni[74].nvs" 18304;
	setAttr ".tgi[0].ni[75].x" 2615.71435546875;
	setAttr ".tgi[0].ni[75].y" 921.4285888671875;
	setAttr ".tgi[0].ni[75].nvs" 18304;
	setAttr ".tgi[0].ni[76].x" 958.5714111328125;
	setAttr ".tgi[0].ni[76].y" 707.14288330078125;
	setAttr ".tgi[0].ni[76].nvs" 18304;
	setAttr ".tgi[0].ni[77].x" 2270;
	setAttr ".tgi[0].ni[77].y" 561.4285888671875;
	setAttr ".tgi[0].ni[77].nvs" 18304;
	setAttr ".tgi[0].ni[78].x" 2270;
	setAttr ".tgi[0].ni[78].y" 410;
	setAttr ".tgi[0].ni[78].nvs" 18304;
	setAttr ".tgi[0].ni[79].x" 2581.428466796875;
	setAttr ".tgi[0].ni[79].y" -1490;
	setAttr ".tgi[0].ni[79].nvs" 18304;
	setAttr ".tgi[0].ni[80].x" 1880;
	setAttr ".tgi[0].ni[80].y" 330;
	setAttr ".tgi[0].ni[80].nvs" 18304;
	setAttr ".tgi[0].ni[81].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[81].y" 278.57144165039063;
	setAttr ".tgi[0].ni[81].nvs" 18304;
	setAttr ".tgi[0].ni[82].x" 1880;
	setAttr ".tgi[0].ni[82].y" 171.42857360839844;
	setAttr ".tgi[0].ni[82].nvs" 18304;
	setAttr ".tgi[0].ni[83].x" 2270;
	setAttr ".tgi[0].ni[83].y" 65.714286804199219;
	setAttr ".tgi[0].ni[83].nvs" 18304;
	setAttr ".tgi[0].ni[84].x" 2615.71435546875;
	setAttr ".tgi[0].ni[84].y" 820;
	setAttr ".tgi[0].ni[84].nvs" 18304;
	setAttr ".tgi[0].ni[85].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[85].y" 1462.857177734375;
	setAttr ".tgi[0].ni[85].nvs" 18304;
	setAttr ".tgi[0].ni[86].x" 651.4285888671875;
	setAttr ".tgi[0].ni[86].y" 685.71429443359375;
	setAttr ".tgi[0].ni[86].nvs" 18304;
	setAttr ".tgi[0].ni[87].x" 1880;
	setAttr ".tgi[0].ni[87].y" 545.71429443359375;
	setAttr ".tgi[0].ni[87].nvs" 18304;
	setAttr ".tgi[0].ni[88].x" 2615.71435546875;
	setAttr ".tgi[0].ni[88].y" 662.85711669921875;
	setAttr ".tgi[0].ni[88].nvs" 18304;
	setAttr ".tgi[0].ni[89].x" 2270;
	setAttr ".tgi[0].ni[89].y" 308.57144165039063;
	setAttr ".tgi[0].ni[89].nvs" 18304;
	setAttr ".tgi[0].ni[90].x" 2532.857177734375;
	setAttr ".tgi[0].ni[90].y" -1100;
	setAttr ".tgi[0].ni[90].nvs" 18304;
	setAttr ".tgi[0].ni[91].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[91].y" 1122.857177734375;
	setAttr ".tgi[0].ni[91].nvs" 18304;
	setAttr ".tgi[0].ni[92].x" 2270;
	setAttr ".tgi[0].ni[92].y" 1201.4285888671875;
	setAttr ".tgi[0].ni[92].nvs" 18304;
	setAttr ".tgi[0].ni[93].x" 958.5714111328125;
	setAttr ".tgi[0].ni[93].y" 361.42855834960938;
	setAttr ".tgi[0].ni[93].nvs" 18304;
	setAttr ".tgi[0].ni[94].x" 2270;
	setAttr ".tgi[0].ni[94].y" 662.85711669921875;
	setAttr ".tgi[0].ni[94].nvs" 18304;
	setAttr ".tgi[0].ni[95].x" 1880;
	setAttr ".tgi[0].ni[95].y" 12.857142448425293;
	setAttr ".tgi[0].ni[95].nvs" 18304;
	setAttr ".tgi[0].ni[96].x" 2610;
	setAttr ".tgi[0].ni[96].y" -2010;
	setAttr ".tgi[0].ni[96].nvs" 18304;
	setAttr ".tgi[0].ni[97].x" 1572.857177734375;
	setAttr ".tgi[0].ni[97].y" 965.71429443359375;
	setAttr ".tgi[0].ni[97].nvs" 18304;
	setAttr ".tgi[0].ni[98].x" 2480;
	setAttr ".tgi[0].ni[98].y" -970;
	setAttr ".tgi[0].ni[98].nvs" 18304;
	setAttr ".tgi[0].ni[99].x" 2434.28564453125;
	setAttr ".tgi[0].ni[99].y" -710;
	setAttr ".tgi[0].ni[99].nvs" 18304;
	setAttr ".tgi[0].ni[100].x" 2577.142822265625;
	setAttr ".tgi[0].ni[100].y" -1360;
	setAttr ".tgi[0].ni[100].nvs" 18304;
	setAttr ".tgi[0].ni[101].x" 2434.28564453125;
	setAttr ".tgi[0].ni[101].y" -580;
	setAttr ".tgi[0].ni[101].nvs" 18304;
	setAttr ".tgi[0].ni[102].x" 1080;
	setAttr ".tgi[0].ni[102].y" -398.57144165039063;
	setAttr ".tgi[0].ni[102].nvs" 18304;
	setAttr ".tgi[0].ni[103].x" 772.85711669921875;
	setAttr ".tgi[0].ni[103].y" -398.57144165039063;
	setAttr ".tgi[0].ni[103].nvs" 18304;
	setAttr ".tgi[0].ni[104].x" 1387.142822265625;
	setAttr ".tgi[0].ni[104].y" -398.57144165039063;
	setAttr ".tgi[0].ni[104].nvs" 18304;
	setAttr ".tgi[0].ni[105].x" 2001.4285888671875;
	setAttr ".tgi[0].ni[105].y" -398.57144165039063;
	setAttr ".tgi[0].ni[105].nvs" 18304;
	setAttr ".tgi[0].ni[106].x" 2308.571533203125;
	setAttr ".tgi[0].ni[106].y" -398.57144165039063;
	setAttr ".tgi[0].ni[106].nvs" 18304;
	setAttr ".tgi[0].ni[107].x" 2615.71435546875;
	setAttr ".tgi[0].ni[107].y" -348.57144165039063;
	setAttr ".tgi[0].ni[107].nvs" 18304;
	setAttr ".tgi[0].ni[108].x" 2615.71435546875;
	setAttr ".tgi[0].ni[108].y" -450;
	setAttr ".tgi[0].ni[108].nvs" 18304;
	setAttr ".tgi[0].ni[109].x" 772.85711669921875;
	setAttr ".tgi[0].ni[109].y" -167.14285278320313;
	setAttr ".tgi[0].ni[109].nvs" 18304;
	setAttr ".tgi[0].ni[110].x" 1080;
	setAttr ".tgi[0].ni[110].y" -167.14285278320313;
	setAttr ".tgi[0].ni[110].nvs" 18304;
	setAttr ".tgi[0].ni[111].x" 1387.142822265625;
	setAttr ".tgi[0].ni[111].y" -167.14285278320313;
	setAttr ".tgi[0].ni[111].nvs" 18304;
	setAttr ".tgi[0].ni[112].x" 1694.2857666015625;
	setAttr ".tgi[0].ni[112].y" -398.57144165039063;
	setAttr ".tgi[0].ni[112].nvs" 18304;
	setAttr ".tgi[0].ni[113].x" 37.142856597900391;
	setAttr ".tgi[0].ni[113].y" 1698.5714111328125;
	setAttr ".tgi[0].ni[113].nvs" 18304;
	setAttr ".tgi[0].ni[114].x" 1694.2857666015625;
	setAttr ".tgi[0].ni[114].y" -167.14285278320313;
	setAttr ".tgi[0].ni[114].nvs" 18304;
	setAttr ".tgi[0].ni[115].x" 2615.71435546875;
	setAttr ".tgi[0].ni[115].y" -2140;
	setAttr ".tgi[0].ni[115].nvs" 18304;
	setAttr ".tgi[0].ni[116].x" 1265.7142333984375;
	setAttr ".tgi[0].ni[116].y" 2040;
	setAttr ".tgi[0].ni[116].nvs" 18304;
	setAttr ".tgi[0].ni[117].x" -2727.142822265625;
	setAttr ".tgi[0].ni[117].y" 918.5714111328125;
	setAttr ".tgi[0].ni[117].nvs" 18304;
	setAttr ".tgi[0].ni[118].x" 344.28570556640625;
	setAttr ".tgi[0].ni[118].y" 1838.5714111328125;
	setAttr ".tgi[0].ni[118].nvs" 18304;
	setAttr ".tgi[0].ni[119].x" -1191.4285888671875;
	setAttr ".tgi[0].ni[119].y" 1264.2857666015625;
	setAttr ".tgi[0].ni[119].nvs" 18304;
	setAttr ".tgi[0].ni[120].x" 2308.571533203125;
	setAttr ".tgi[0].ni[120].y" -167.14285278320313;
	setAttr ".tgi[0].ni[120].nvs" 18304;
	setAttr ".tgi[0].ni[121].x" 2001.4285888671875;
	setAttr ".tgi[0].ni[121].y" -167.14285278320313;
	setAttr ".tgi[0].ni[121].nvs" 18304;
	setAttr ".tgi[0].ni[122].x" 2615.71435546875;
	setAttr ".tgi[0].ni[122].y" -117.14286041259766;
	setAttr ".tgi[0].ni[122].nvs" 18304;
	setAttr ".tgi[0].ni[123].x" -1498.5714111328125;
	setAttr ".tgi[0].ni[123].y" 1192.857177734375;
	setAttr ".tgi[0].ni[123].nvs" 18304;
	setAttr ".tgi[0].ni[124].x" -884.28570556640625;
	setAttr ".tgi[0].ni[124].y" 1334.2857666015625;
	setAttr ".tgi[0].ni[124].nvs" 18304;
	setAttr ".tgi[0].ni[125].x" 2615.71435546875;
	setAttr ".tgi[0].ni[125].y" -218.57142639160156;
	setAttr ".tgi[0].ni[125].nvs" 18304;
	setAttr ".tgi[0].ni[126].x" 651.4285888671875;
	setAttr ".tgi[0].ni[126].y" 1988.5714111328125;
	setAttr ".tgi[0].ni[126].nvs" 18304;
	setAttr ".tgi[0].ni[127].x" -2420;
	setAttr ".tgi[0].ni[127].y" 1004.2857055664063;
	setAttr ".tgi[0].ni[127].nvs" 18304;
	setAttr ".tgi[0].ni[128].x" -2112.857177734375;
	setAttr ".tgi[0].ni[128].y" 1065.7142333984375;
	setAttr ".tgi[0].ni[128].nvs" 18304;
	setAttr ".tgi[0].ni[129].x" -1805.7142333984375;
	setAttr ".tgi[0].ni[129].y" 1128.5714111328125;
	setAttr ".tgi[0].ni[129].nvs" 18304;
	setAttr ".tgi[0].ni[130].x" -577.14288330078125;
	setAttr ".tgi[0].ni[130].y" 1397.142822265625;
	setAttr ".tgi[0].ni[130].nvs" 18304;
	setAttr ".tgi[0].ni[131].x" -270;
	setAttr ".tgi[0].ni[131].y" 1552.857177734375;
	setAttr ".tgi[0].ni[131].nvs" 18304;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo1";
	rename -uid "45BB888D-4CC6-FCDE-C153-67BC667AAC18";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 0 -17.460316766506807 ;
	setAttr ".tgi[0].vh" -type "double2" 73.015870114483008 0 ;
	setAttr -s 132 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -55.714286804199219;
	setAttr ".tgi[0].ni[0].y" 87.142860412597656;
	setAttr ".tgi[0].ni[0].nvs" 1922;
	setAttr ".tgi[0].ni[1].x" 990;
	setAttr ".tgi[0].ni[1].y" 8904.2861328125;
	setAttr ".tgi[0].ni[1].nvs" 2034;
	setAttr ".tgi[0].ni[2].x" 1742.857177734375;
	setAttr ".tgi[0].ni[2].y" -4145.71435546875;
	setAttr ".tgi[0].ni[2].nvs" 2034;
	setAttr ".tgi[0].ni[3].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[3].y" 10927.142578125;
	setAttr ".tgi[0].ni[3].nvs" 2034;
	setAttr ".tgi[0].ni[4].x" 2377.142822265625;
	setAttr ".tgi[0].ni[4].y" -3514.28564453125;
	setAttr ".tgi[0].ni[4].nvs" 2034;
	setAttr ".tgi[0].ni[5].x" 2694.28564453125;
	setAttr ".tgi[0].ni[5].y" -2948.571533203125;
	setAttr ".tgi[0].ni[5].nvs" 2034;
	setAttr ".tgi[0].ni[6].x" 2694.28564453125;
	setAttr ".tgi[0].ni[6].y" -5590;
	setAttr ".tgi[0].ni[6].nvs" 2034;
	setAttr ".tgi[0].ni[7].x" 1307.142822265625;
	setAttr ".tgi[0].ni[7].y" 10605.7138671875;
	setAttr ".tgi[0].ni[7].nvs" 2034;
	setAttr ".tgi[0].ni[8].x" 1307.142822265625;
	setAttr ".tgi[0].ni[8].y" 11105.7138671875;
	setAttr ".tgi[0].ni[8].nvs" 2034;
	setAttr ".tgi[0].ni[9].x" 2694.28564453125;
	setAttr ".tgi[0].ni[9].y" 12375.7138671875;
	setAttr ".tgi[0].ni[9].nvs" 2034;
	setAttr ".tgi[0].ni[10].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[10].y" 10742.857421875;
	setAttr ".tgi[0].ni[10].nvs" 2034;
	setAttr ".tgi[0].ni[11].x" 38.571430206298828;
	setAttr ".tgi[0].ni[11].y" 6182.85693359375;
	setAttr ".tgi[0].ni[11].nvs" 2034;
	setAttr ".tgi[0].ni[12].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[12].y" 11242.857421875;
	setAttr ".tgi[0].ni[12].nvs" 2034;
	setAttr ".tgi[0].ni[13].x" 1425.7142333984375;
	setAttr ".tgi[0].ni[13].y" -4461.4287109375;
	setAttr ".tgi[0].ni[13].nvs" 2034;
	setAttr ".tgi[0].ni[14].x" 2694.28564453125;
	setAttr ".tgi[0].ni[14].y" -3448.571533203125;
	setAttr ".tgi[0].ni[14].nvs" 2034;
	setAttr ".tgi[0].ni[15].x" -2181.428466796875;
	setAttr ".tgi[0].ni[15].y" -10;
	setAttr ".tgi[0].ni[15].nvs" 2034;
	setAttr ".tgi[0].ni[16].x" 1108.5714111328125;
	setAttr ".tgi[0].ni[16].y" -4777.14306640625;
	setAttr ".tgi[0].ni[16].nvs" 2034;
	setAttr ".tgi[0].ni[17].x" 1425.7142333984375;
	setAttr ".tgi[0].ni[17].y" -7098.5712890625;
	setAttr ".tgi[0].ni[17].nvs" 2034;
	setAttr ".tgi[0].ni[18].x" -1547.142822265625;
	setAttr ".tgi[0].ni[18].y" 1627.142822265625;
	setAttr ".tgi[0].ni[18].nvs" 2034;
	setAttr ".tgi[0].ni[19].x" 791.4285888671875;
	setAttr ".tgi[0].ni[19].y" -7730;
	setAttr ".tgi[0].ni[19].nvs" 2034;
	setAttr ".tgi[0].ni[20].x" -278.57144165039063;
	setAttr ".tgi[0].ni[20].y" 4990;
	setAttr ".tgi[0].ni[20].nvs" 2034;
	setAttr ".tgi[0].ni[21].x" -912.85711669921875;
	setAttr ".tgi[0].ni[21].y" 3260;
	setAttr ".tgi[0].ni[21].nvs" 2034;
	setAttr ".tgi[0].ni[22].x" 2377.142822265625;
	setAttr ".tgi[0].ni[22].y" -6151.4287109375;
	setAttr ".tgi[0].ni[22].nvs" 2034;
	setAttr ".tgi[0].ni[23].x" 791.4285888671875;
	setAttr ".tgi[0].ni[23].y" -5092.85693359375;
	setAttr ".tgi[0].ni[23].nvs" 2034;
	setAttr ".tgi[0].ni[24].x" 2694.28564453125;
	setAttr ".tgi[0].ni[24].y" -6081.4287109375;
	setAttr ".tgi[0].ni[24].nvs" 2034;
	setAttr ".tgi[0].ni[25].x" 2704.28564453125;
	setAttr ".tgi[0].ni[25].y" -11874.2861328125;
	setAttr ".tgi[0].ni[25].nvs" 1923;
	setAttr ".tgi[0].ni[26].x" 1108.5714111328125;
	setAttr ".tgi[0].ni[26].y" -7414.28564453125;
	setAttr ".tgi[0].ni[26].nvs" 2034;
	setAttr ".tgi[0].ni[27].x" -2498.571533203125;
	setAttr ".tgi[0].ni[27].y" -834.28570556640625;
	setAttr ".tgi[0].ni[27].nvs" 2034;
	setAttr ".tgi[0].ni[28].x" -1864.2857666015625;
	setAttr ".tgi[0].ni[28].y" 804.28570556640625;
	setAttr ".tgi[0].ni[28].nvs" 2034;
	setAttr ".tgi[0].ni[29].x" -1230;
	setAttr ".tgi[0].ni[29].y" 2438.571533203125;
	setAttr ".tgi[0].ni[29].nvs" 2034;
	setAttr ".tgi[0].ni[30].x" 672.85711669921875;
	setAttr ".tgi[0].ni[30].y" 8842.857421875;
	setAttr ".tgi[0].ni[30].nvs" 2034;
	setAttr ".tgi[0].ni[31].x" 2694.28564453125;
	setAttr ".tgi[0].ni[31].y" 11875.7138671875;
	setAttr ".tgi[0].ni[31].nvs" 2034;
	setAttr ".tgi[0].ni[32].x" 2304.28564453125;
	setAttr ".tgi[0].ni[32].y" 12058.5712890625;
	setAttr ".tgi[0].ni[32].nvs" 2034;
	setAttr ".tgi[0].ni[33].x" -2815.71435546875;
	setAttr ".tgi[0].ni[33].y" -1638.5714111328125;
	setAttr ".tgi[0].ni[33].nvs" 2034;
	setAttr ".tgi[0].ni[34].x" -595.71429443359375;
	setAttr ".tgi[0].ni[34].y" 4071.428466796875;
	setAttr ".tgi[0].ni[34].nvs" 2034;
	setAttr ".tgi[0].ni[35].x" 1307.142822265625;
	setAttr ".tgi[0].ni[35].y" 10114.2861328125;
	setAttr ".tgi[0].ni[35].nvs" 2034;
	setAttr ".tgi[0].ni[36].x" 2060;
	setAttr ".tgi[0].ni[36].y" -3830;
	setAttr ".tgi[0].ni[36].nvs" 2034;
	setAttr ".tgi[0].ni[37].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[37].y" 11741.4287109375;
	setAttr ".tgi[0].ni[37].nvs" 2034;
	setAttr ".tgi[0].ni[38].x" 2060;
	setAttr ".tgi[0].ni[38].y" -6467.14306640625;
	setAttr ".tgi[0].ni[38].nvs" 2034;
	setAttr ".tgi[0].ni[39].x" 2304.28564453125;
	setAttr ".tgi[0].ni[39].y" 11060;
	setAttr ".tgi[0].ni[39].nvs" 2034;
	setAttr ".tgi[0].ni[40].x" 2694.28564453125;
	setAttr ".tgi[0].ni[40].y" 11375.7138671875;
	setAttr ".tgi[0].ni[40].nvs" 2034;
	setAttr ".tgi[0].ni[41].x" 1307.142822265625;
	setAttr ".tgi[0].ni[41].y" 9122.857421875;
	setAttr ".tgi[0].ni[41].nvs" 2034;
	setAttr ".tgi[0].ni[42].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[42].y" 9747.142578125;
	setAttr ".tgi[0].ni[42].nvs" 2034;
	setAttr ".tgi[0].ni[43].x" 2304.28564453125;
	setAttr ".tgi[0].ni[43].y" 11558.5712890625;
	setAttr ".tgi[0].ni[43].nvs" 2034;
	setAttr ".tgi[0].ni[44].x" 355.71429443359375;
	setAttr ".tgi[0].ni[44].y" 7188.5712890625;
	setAttr ".tgi[0].ni[44].nvs" 2034;
	setAttr ".tgi[0].ni[45].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[45].y" 11422.857421875;
	setAttr ".tgi[0].ni[45].nvs" 2034;
	setAttr ".tgi[0].ni[46].x" 2304.28564453125;
	setAttr ".tgi[0].ni[46].y" 10062.857421875;
	setAttr ".tgi[0].ni[46].nvs" 2034;
	setAttr ".tgi[0].ni[47].x" 1742.857177734375;
	setAttr ".tgi[0].ni[47].y" -6782.85693359375;
	setAttr ".tgi[0].ni[47].nvs" 2034;
	setAttr ".tgi[0].ni[48].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[48].y" 10427.142578125;
	setAttr ".tgi[0].ni[48].nvs" 2034;
	setAttr ".tgi[0].ni[49].x" 1307.142822265625;
	setAttr ".tgi[0].ni[49].y" 9614.2861328125;
	setAttr ".tgi[0].ni[49].nvs" 2034;
	setAttr ".tgi[0].ni[50].x" 2304.28564453125;
	setAttr ".tgi[0].ni[50].y" 10560;
	setAttr ".tgi[0].ni[50].nvs" 2034;
	setAttr ".tgi[0].ni[51].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[51].y" 9437.142578125;
	setAttr ".tgi[0].ni[51].nvs" 2034;
	setAttr ".tgi[0].ni[52].x" 2694.28564453125;
	setAttr ".tgi[0].ni[52].y" 10875.7138671875;
	setAttr ".tgi[0].ni[52].nvs" 2034;
	setAttr ".tgi[0].ni[53].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[53].y" 9928.5712890625;
	setAttr ".tgi[0].ni[53].nvs" 2034;
	setAttr ".tgi[0].ni[54].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[54].y" 7948.5712890625;
	setAttr ".tgi[0].ni[54].nvs" 2546;
	setAttr ".tgi[0].ni[55].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[55].y" 6718.5712890625;
	setAttr ".tgi[0].ni[55].nvs" 2034;
	setAttr ".tgi[0].ni[56].x" 2694.28564453125;
	setAttr ".tgi[0].ni[56].y" 10378.5712890625;
	setAttr ".tgi[0].ni[56].nvs" 2034;
	setAttr ".tgi[0].ni[57].x" 672.85711669921875;
	setAttr ".tgi[0].ni[57].y" 8342.857421875;
	setAttr ".tgi[0].ni[57].nvs" 2034;
	setAttr ".tgi[0].ni[58].x" 2304.28564453125;
	setAttr ".tgi[0].ni[58].y" 6660;
	setAttr ".tgi[0].ni[58].nvs" 2546;
	setAttr ".tgi[0].ni[59].x" 990;
	setAttr ".tgi[0].ni[59].y" 8168.5712890625;
	setAttr ".tgi[0].ni[59].nvs" 2034;
	setAttr ".tgi[0].ni[60].x" 1307.142822265625;
	setAttr ".tgi[0].ni[60].y" 8065.71435546875;
	setAttr ".tgi[0].ni[60].nvs" 2034;
	setAttr ".tgi[0].ni[61].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[61].y" 10247.142578125;
	setAttr ".tgi[0].ni[61].nvs" 2034;
	setAttr ".tgi[0].ni[62].x" 2304.28564453125;
	setAttr ".tgi[0].ni[62].y" 8264.2861328125;
	setAttr ".tgi[0].ni[62].nvs" 2034;
	setAttr ".tgi[0].ni[63].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[63].y" 8258.5712890625;
	setAttr ".tgi[0].ni[63].nvs" 2034;
	setAttr ".tgi[0].ni[64].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[64].y" 8448.5712890625;
	setAttr ".tgi[0].ni[64].nvs" 2034;
	setAttr ".tgi[0].ni[65].x" 1307.142822265625;
	setAttr ".tgi[0].ni[65].y" 6380;
	setAttr ".tgi[0].ni[65].nvs" 2034;
	setAttr ".tgi[0].ni[66].x" 2694.28564453125;
	setAttr ".tgi[0].ni[66].y" 9878.5712890625;
	setAttr ".tgi[0].ni[66].nvs" 2034;
	setAttr ".tgi[0].ni[67].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[67].y" 5400;
	setAttr ".tgi[0].ni[67].nvs" 2034;
	setAttr ".tgi[0].ni[68].x" 2304.28564453125;
	setAttr ".tgi[0].ni[68].y" 8787.142578125;
	setAttr ".tgi[0].ni[68].nvs" 2034;
	setAttr ".tgi[0].ni[69].x" 2694.28564453125;
	setAttr ".tgi[0].ni[69].y" 9125.7138671875;
	setAttr ".tgi[0].ni[69].nvs" 2034;
	setAttr ".tgi[0].ni[70].x" 355.71429443359375;
	setAttr ".tgi[0].ni[70].y" 6372.85693359375;
	setAttr ".tgi[0].ni[70].nvs" 2034;
	setAttr ".tgi[0].ni[71].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[71].y" 6142.85693359375;
	setAttr ".tgi[0].ni[71].nvs" 2034;
	setAttr ".tgi[0].ni[72].x" 1307.142822265625;
	setAttr ".tgi[0].ni[72].y" 7337.14306640625;
	setAttr ".tgi[0].ni[72].nvs" 2034;
	setAttr ".tgi[0].ni[73].x" 38.571430206298828;
	setAttr ".tgi[0].ni[73].y" 5432.85693359375;
	setAttr ".tgi[0].ni[73].nvs" 2034;
	setAttr ".tgi[0].ni[74].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[74].y" 7210;
	setAttr ".tgi[0].ni[74].nvs" 2034;
	setAttr ".tgi[0].ni[75].x" 2694.28564453125;
	setAttr ".tgi[0].ni[75].y" 8012.85693359375;
	setAttr ".tgi[0].ni[75].nvs" 2034;
	setAttr ".tgi[0].ni[76].x" 672.85711669921875;
	setAttr ".tgi[0].ni[76].y" 7328.5712890625;
	setAttr ".tgi[0].ni[76].nvs" 2034;
	setAttr ".tgi[0].ni[77].x" 2694.28564453125;
	setAttr ".tgi[0].ni[77].y" 7475.71435546875;
	setAttr ".tgi[0].ni[77].nvs" 2034;
	setAttr ".tgi[0].ni[78].x" 2304.28564453125;
	setAttr ".tgi[0].ni[78].y" 5921.4287109375;
	setAttr ".tgi[0].ni[78].nvs" 2034;
	setAttr ".tgi[0].ni[79].x" 1307.142822265625;
	setAttr ".tgi[0].ni[79].y" 8622.857421875;
	setAttr ".tgi[0].ni[79].nvs" 2034;
	setAttr ".tgi[0].ni[80].x" 2694.28564453125;
	setAttr ".tgi[0].ni[80].y" 6241.4287109375;
	setAttr ".tgi[0].ni[80].nvs" 2034;
	setAttr ".tgi[0].ni[81].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[81].y" 8937.142578125;
	setAttr ".tgi[0].ni[81].nvs" 2034;
	setAttr ".tgi[0].ni[82].x" 2304.28564453125;
	setAttr ".tgi[0].ni[82].y" 7674.28564453125;
	setAttr ".tgi[0].ni[82].nvs" 2034;
	setAttr ".tgi[0].ni[83].x" 2304.28564453125;
	setAttr ".tgi[0].ni[83].y" 9562.857421875;
	setAttr ".tgi[0].ni[83].nvs" 2034;
	setAttr ".tgi[0].ni[84].x" 990;
	setAttr ".tgi[0].ni[84].y" 6690;
	setAttr ".tgi[0].ni[84].nvs" 2034;
	setAttr ".tgi[0].ni[85].x" 1307.142822265625;
	setAttr ".tgi[0].ni[85].y" 5888.5712890625;
	setAttr ".tgi[0].ni[85].nvs" 2034;
	setAttr ".tgi[0].ni[86].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[86].y" 5642.85693359375;
	setAttr ".tgi[0].ni[86].nvs" 2034;
	setAttr ".tgi[0].ni[87].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[87].y" 7425.71435546875;
	setAttr ".tgi[0].ni[87].nvs" 2034;
	setAttr ".tgi[0].ni[88].x" -278.57144165039063;
	setAttr ".tgi[0].ni[88].y" 4490;
	setAttr ".tgi[0].ni[88].nvs" 2034;
	setAttr ".tgi[0].ni[89].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[89].y" 5900;
	setAttr ".tgi[0].ni[89].nvs" 2034;
	setAttr ".tgi[0].ni[90].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[90].y" 9247.142578125;
	setAttr ".tgi[0].ni[90].nvs" 2034;
	setAttr ".tgi[0].ni[91].x" 2304.28564453125;
	setAttr ".tgi[0].ni[91].y" 7160;
	setAttr ".tgi[0].ni[91].nvs" 2034;
	setAttr ".tgi[0].ni[92].x" 2304.28564453125;
	setAttr ".tgi[0].ni[92].y" 5430;
	setAttr ".tgi[0].ni[92].nvs" 2034;
	setAttr ".tgi[0].ni[93].x" 2694.28564453125;
	setAttr ".tgi[0].ni[93].y" 5741.4287109375;
	setAttr ".tgi[0].ni[93].nvs" 2034;
	setAttr ".tgi[0].ni[94].x" 1307.142822265625;
	setAttr ".tgi[0].ni[94].y" 5397.14306640625;
	setAttr ".tgi[0].ni[94].nvs" 2034;
	setAttr ".tgi[0].ni[95].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[95].y" 5142.85693359375;
	setAttr ".tgi[0].ni[95].nvs" 2034;
	setAttr ".tgi[0].ni[96].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[96].y" 4908.5712890625;
	setAttr ".tgi[0].ni[96].nvs" 2034;
	setAttr ".tgi[0].ni[97].x" 2304.28564453125;
	setAttr ".tgi[0].ni[97].y" 4930;
	setAttr ".tgi[0].ni[97].nvs" 2034;
	setAttr ".tgi[0].ni[98].x" 2694.28564453125;
	setAttr ".tgi[0].ni[98].y" 5250;
	setAttr ".tgi[0].ni[98].nvs" 2034;
	setAttr ".tgi[0].ni[99].x" 2694.28564453125;
	setAttr ".tgi[0].ni[99].y" 4750;
	setAttr ".tgi[0].ni[99].nvs" 2034;
	setAttr ".tgi[0].ni[100].x" 2670;
	setAttr ".tgi[0].ni[100].y" -10357.142578125;
	setAttr ".tgi[0].ni[100].nvs" 2034;
	setAttr ".tgi[0].ni[101].x" 2694.28564453125;
	setAttr ".tgi[0].ni[101].y" 4250;
	setAttr ".tgi[0].ni[101].nvs" 2034;
	setAttr ".tgi[0].ni[102].x" 2621.428466796875;
	setAttr ".tgi[0].ni[102].y" -9255.7138671875;
	setAttr ".tgi[0].ni[102].nvs" 2034;
	setAttr ".tgi[0].ni[103].x" 2304.28564453125;
	setAttr ".tgi[0].ni[103].y" -292.85714721679688;
	setAttr ".tgi[0].ni[103].nvs" 2546;
	setAttr ".tgi[0].ni[104].x" 2304.28564453125;
	setAttr ".tgi[0].ni[104].y" -1787.142822265625;
	setAttr ".tgi[0].ni[104].nvs" 2034;
	setAttr ".tgi[0].ni[105].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[105].y" -387.14285278320313;
	setAttr ".tgi[0].ni[105].nvs" 2546;
	setAttr ".tgi[0].ni[106].x" 2304.28564453125;
	setAttr ".tgi[0].ni[106].y" 1497.142822265625;
	setAttr ".tgi[0].ni[106].nvs" 2034;
	setAttr ".tgi[0].ni[107].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[107].y" 685.71429443359375;
	setAttr ".tgi[0].ni[107].nvs" 2034;
	setAttr ".tgi[0].ni[108].x" 990;
	setAttr ".tgi[0].ni[108].y" -1588.5714111328125;
	setAttr ".tgi[0].ni[108].nvs" 2034;
	setAttr ".tgi[0].ni[109].x" 1307.142822265625;
	setAttr ".tgi[0].ni[109].y" -1515.7142333984375;
	setAttr ".tgi[0].ni[109].nvs" 2034;
	setAttr ".tgi[0].ni[110].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[110].y" 194.28572082519531;
	setAttr ".tgi[0].ni[110].nvs" 2034;
	setAttr ".tgi[0].ni[111].x" 2694.28564453125;
	setAttr ".tgi[0].ni[111].y" 1812.857177734375;
	setAttr ".tgi[0].ni[111].nvs" 2034;
	setAttr ".tgi[0].ni[112].x" 2698.571533203125;
	setAttr ".tgi[0].ni[112].y" -11625.7138671875;
	setAttr ".tgi[0].ni[112].nvs" 1922;
	setAttr ".tgi[0].ni[113].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[113].y" -1774.2857666015625;
	setAttr ".tgi[0].ni[113].nvs" 2034;
	setAttr ".tgi[0].ni[114].x" 990;
	setAttr ".tgi[0].ni[114].y" -87.142860412597656;
	setAttr ".tgi[0].ni[114].nvs" 2034;
	setAttr ".tgi[0].ni[115].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[115].y" -1362.857177734375;
	setAttr ".tgi[0].ni[115].nvs" 2034;
	setAttr ".tgi[0].ni[116].x" 2304.28564453125;
	setAttr ".tgi[0].ni[116].y" -1040;
	setAttr ".tgi[0].ni[116].nvs" 2546;
	setAttr ".tgi[0].ni[117].x" 2634.28564453125;
	setAttr ".tgi[0].ni[117].y" -9851.4287109375;
	setAttr ".tgi[0].ni[117].nvs" 1922;
	setAttr ".tgi[0].ni[118].x" 2690;
	setAttr ".tgi[0].ni[118].y" -11368.5712890625;
	setAttr ".tgi[0].ni[118].nvs" 1922;
	setAttr ".tgi[0].ni[119].x" 2522.857177734375;
	setAttr ".tgi[0].ni[119].y" -8741.4287109375;
	setAttr ".tgi[0].ni[119].nvs" 1922;
	setAttr ".tgi[0].ni[120].x" 1307.142822265625;
	setAttr ".tgi[0].ni[120].y" 2.8571429252624512;
	setAttr ".tgi[0].ni[120].nvs" 2034;
	setAttr ".tgi[0].ni[121].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[121].y" 1177.142822265625;
	setAttr ".tgi[0].ni[121].nvs" 2034;
	setAttr ".tgi[0].ni[122].x" 2522.857177734375;
	setAttr ".tgi[0].ni[122].y" -8484.2861328125;
	setAttr ".tgi[0].ni[122].nvs" 1922;
	setAttr ".tgi[0].ni[123].x" 2522.857177734375;
	setAttr ".tgi[0].ni[123].y" -8227.142578125;
	setAttr ".tgi[0].ni[123].nvs" 1922;
	setAttr ".tgi[0].ni[124].x" 1624.2857666015625;
	setAttr ".tgi[0].ni[124].y" -157.14285278320313;
	setAttr ".tgi[0].ni[124].nvs" 2034;
	setAttr ".tgi[0].ni[125].x" 2568.571533203125;
	setAttr ".tgi[0].ni[125].y" -8998.5712890625;
	setAttr ".tgi[0].ni[125].nvs" 1922;
	setAttr ".tgi[0].ni[126].x" 2672.857177734375;
	setAttr ".tgi[0].ni[126].y" -10952.857421875;
	setAttr ".tgi[0].ni[126].nvs" 1922;
	setAttr ".tgi[0].ni[127].x" 2694.28564453125;
	setAttr ".tgi[0].ni[127].y" 1312.857177734375;
	setAttr ".tgi[0].ni[127].nvs" 2034;
	setAttr ".tgi[0].ni[128].x" 2304.28564453125;
	setAttr ".tgi[0].ni[128].y" 297.14285278320313;
	setAttr ".tgi[0].ni[128].nvs" 2034;
	setAttr ".tgi[0].ni[129].x" 2304.28564453125;
	setAttr ".tgi[0].ni[129].y" 997.14288330078125;
	setAttr ".tgi[0].ni[129].nvs" 2034;
	setAttr ".tgi[0].ni[130].x" 2665.71435546875;
	setAttr ".tgi[0].ni[130].y" -10108.5712890625;
	setAttr ".tgi[0].ni[130].nvs" 1922;
	setAttr ".tgi[0].ni[131].x" 1941.4285888671875;
	setAttr ".tgi[0].ni[131].y" -2181.428466796875;
	setAttr ".tgi[0].ni[131].nvs" 2546;
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
	setAttr -s 10 ".r";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "ankle_l_pivot.s" "bankIn_l_pivot.is";
connectAttr "bankIn_l_pivot.s" "bankOut_l_pivot.is";
connectAttr "bankOut_l_pivot.s" "heel_l_pivot.is";
connectAttr "heel_l_pivot.s" "ball_l_pivot.is";
connectAttr "ball_l_pivot.s" "toe_l_pivot.is";
connectAttr "toe_l_pivot.s" "toeBend_l_pivot.is";
connectAttr "toe_l_pivot.s" "ballRoll_l_pivot.is";
connectAttr "ankle_r_pivot.s" "bankIn_r_pivot.is";
connectAttr "bankIn_r_pivot.s" "bankOut_r_pivot.is";
connectAttr "bankOut_r_pivot.s" "heel_r_pivot.is";
connectAttr "heel_r_pivot.s" "ball_r_pivot.is";
connectAttr "ball_r_pivot.s" "toe_r_pivot.is";
connectAttr "toe_r_pivot.s" "ballRoll_r_pivot.is";
connectAttr "toe_r_pivot.s" "toeBend_r_pivot.is";
connectAttr "hips_bind.s" "spine_0_bind.is";
connectAttr "spine_0_bind.s" "spine_1_bind.is";
connectAttr "spine_1_bind.s" "spine_2_bind.is";
connectAttr "spine_2_bind.s" "spine_3_bind.is";
connectAttr "spine_3_bind.s" "spine_4_bind.is";
connectAttr "spine_4_bind.s" "spine_5_bind.is";
connectAttr "spine_5_bind.s" "chest_bind.is";
connectAttr "chest_bind.s" "clavicle_l_bind.is";
connectAttr "clavicle_l_bind.s" "shoulder_l_bind.is";
connectAttr "shoulder_l_bind.s" "elbow_l_bind.is";
connectAttr "elbow_l_bind.s" "wrist_l_bind.is";
connectAttr "wrist_l_bind.s" "ring_001_l_bind.is";
connectAttr "ring_001_l_bind.s" "ring_002_l_bind.is";
connectAttr "ring_002_l_bind.s" "ring_003_l_bind.is";
connectAttr "ring_003_l_bind.s" "ring_004_l_bind.is";
connectAttr "ring_004_l_bind.s" "ring_005_l_bind.is";
connectAttr "wrist_l_bind.s" "middle_001_l_bind.is";
connectAttr "middle_001_l_bind.s" "middle_002_l_bind.is";
connectAttr "middle_002_l_bind.s" "middle_003_l_bind.is";
connectAttr "middle_003_l_bind.s" "middle_004_l_bind.is";
connectAttr "middle_004_l_bind.s" "middle_005_l_bind.is";
connectAttr "wrist_l_bind.s" "index_001_l_bind.is";
connectAttr "index_001_l_bind.s" "index_002_l_bind.is";
connectAttr "index_002_l_bind.s" "index_003_l_bind.is";
connectAttr "index_003_l_bind.s" "index_004_l_bind.is";
connectAttr "index_004_l_bind.s" "index_005_l_bind.is";
connectAttr "wrist_l_bind.s" "pinkyCup_l_bind.is";
connectAttr "pinkyCup_l_bind.s" "pinky_001_l_bind.is";
connectAttr "pinky_001_l_bind.s" "pinky_002_l_bind.is";
connectAttr "pinky_002_l_bind.s" "pinky_003_l_bind.is";
connectAttr "pinky_003_l_bind.s" "pinky_004_l_bind.is";
connectAttr "pinky_004_l_bind.s" "pinky_005_l_bind.is";
connectAttr "wrist_l_bind.s" "thumbCup_l_bind.is";
connectAttr "thumbCup_l_bind.s" "thumb_001_l_bind.is";
connectAttr "thumb_001_l_bind.s" "thumb_002_l_bind.is";
connectAttr "thumb_002_l_bind.s" "thumb_003_l_bind.is";
connectAttr "thumb_003_l_bind.s" "thumb_004_l_bind.is";
connectAttr "wrist_l_bind.s" "wristTwist_l_bind.is";
connectAttr "wristTwist_l_bind_aimConstraint1.crx" "wristTwist_l_bind.rx";
connectAttr "wristTwist_l_bind_aimConstraint1.cry" "wristTwist_l_bind.ry";
connectAttr "wristTwist_l_bind_aimConstraint1.crz" "wristTwist_l_bind.rz";
connectAttr "wristTwist_l_bind.pim" "wristTwist_l_bind_aimConstraint1.cpim";
connectAttr "wristTwist_l_bind.t" "wristTwist_l_bind_aimConstraint1.ct";
connectAttr "wristTwist_l_bind.rp" "wristTwist_l_bind_aimConstraint1.crp";
connectAttr "wristTwist_l_bind.rpt" "wristTwist_l_bind_aimConstraint1.crt";
connectAttr "wristTwist_l_bind.ro" "wristTwist_l_bind_aimConstraint1.cro";
connectAttr "wristTwist_l_bind.jo" "wristTwist_l_bind_aimConstraint1.cjo";
connectAttr "wristTwist_l_bind.is" "wristTwist_l_bind_aimConstraint1.is";
connectAttr "elbow_l_bind.t" "wristTwist_l_bind_aimConstraint1.tg[0].tt";
connectAttr "elbow_l_bind.rp" "wristTwist_l_bind_aimConstraint1.tg[0].trp";
connectAttr "elbow_l_bind.rpt" "wristTwist_l_bind_aimConstraint1.tg[0].trt";
connectAttr "elbow_l_bind.pm" "wristTwist_l_bind_aimConstraint1.tg[0].tpm";
connectAttr "wristTwist_l_bind_aimConstraint1.w0" "wristTwist_l_bind_aimConstraint1.tg[0].tw"
		;
connectAttr "shoulder_l_bind.jo" "shoulderNoTwist_l_bind.jo";
connectAttr "clavicle_l_bind.s" "shoulderNoTwist_l_bind.is";
connectAttr "shoulder_l_bind.t" "shoulderNoTwist_l_bind.t";
connectAttr "shoulder_l_bind.ro" "shoulderNoTwist_l_bind.ro";
connectAttr "shoulderNoTwist_l_bind_aimConstraint1.crx" "shoulderNoTwist_l_bind.rx"
		;
connectAttr "shoulderNoTwist_l_bind_aimConstraint1.cry" "shoulderNoTwist_l_bind.ry"
		;
connectAttr "shoulderNoTwist_l_bind_aimConstraint1.crz" "shoulderNoTwist_l_bind.rz"
		;
connectAttr "shoulderNoTwist_l_bind.pim" "shoulderNoTwist_l_bind_aimConstraint1.cpim"
		;
connectAttr "shoulderNoTwist_l_bind.t" "shoulderNoTwist_l_bind_aimConstraint1.ct"
		;
connectAttr "shoulderNoTwist_l_bind.rp" "shoulderNoTwist_l_bind_aimConstraint1.crp"
		;
connectAttr "shoulderNoTwist_l_bind.rpt" "shoulderNoTwist_l_bind_aimConstraint1.crt"
		;
connectAttr "shoulderNoTwist_l_bind.ro" "shoulderNoTwist_l_bind_aimConstraint1.cro"
		;
connectAttr "shoulderNoTwist_l_bind.jo" "shoulderNoTwist_l_bind_aimConstraint1.cjo"
		;
connectAttr "shoulderNoTwist_l_bind.is" "shoulderNoTwist_l_bind_aimConstraint1.is"
		;
connectAttr "elbow_l_bind.t" "shoulderNoTwist_l_bind_aimConstraint1.tg[0].tt";
connectAttr "elbow_l_bind.rp" "shoulderNoTwist_l_bind_aimConstraint1.tg[0].trp";
connectAttr "elbow_l_bind.rpt" "shoulderNoTwist_l_bind_aimConstraint1.tg[0].trt"
		;
connectAttr "elbow_l_bind.pm" "shoulderNoTwist_l_bind_aimConstraint1.tg[0].tpm";
connectAttr "shoulderNoTwist_l_bind_aimConstraint1.w0" "shoulderNoTwist_l_bind_aimConstraint1.tg[0].tw"
		;
connectAttr "chest_bind.s" "neck_0_bind.is";
connectAttr "neck_0_bind.s" "neck_1_bind.is";
connectAttr "neck_1_bind.s" "neck_2_bind.is";
connectAttr "neck_2_bind.s" "neck_3_bind.is";
connectAttr "neck_3_bind.s" "skull_bind.is";
connectAttr "skull_bind.s" "eyeSocket_l_bind.is";
connectAttr "eyeSocket_l_bind.s" "eye_l_bind.is";
connectAttr "skull_bind.s" "eyeSocket_r_bind.is";
connectAttr "eyeSocket_r_bind.s" "eye_r_bind.is";
connectAttr "chest_bind.s" "clavicle_r_bind.is";
connectAttr "clavicle_r_bind.s" "shoulder_r_bind.is";
connectAttr "shoulder_r_bind.s" "elbow_r_bind.is";
connectAttr "elbow_r_bind.s" "wrist_r_bind.is";
connectAttr "wrist_r_bind.s" "ring_001_r_bind.is";
connectAttr "ring_001_r_bind.s" "ring_002_r_bind.is";
connectAttr "ring_002_r_bind.s" "ring_003_r_bind.is";
connectAttr "ring_003_r_bind.s" "ring_004_r_bind.is";
connectAttr "ring_004_r_bind.s" "ring_005_r_bind.is";
connectAttr "wrist_r_bind.s" "middle_001_r_bind.is";
connectAttr "middle_001_r_bind.s" "middle_002_r_bind.is";
connectAttr "middle_002_r_bind.s" "middle_003_r_bind.is";
connectAttr "middle_003_r_bind.s" "middle_004_r_bind.is";
connectAttr "middle_004_r_bind.s" "middle_005_r_bind.is";
connectAttr "wrist_r_bind.s" "index_001_r_bind.is";
connectAttr "index_001_r_bind.s" "index_002_r_bind.is";
connectAttr "index_002_r_bind.s" "index_003_r_bind.is";
connectAttr "index_003_r_bind.s" "index_004_r_bind.is";
connectAttr "index_004_r_bind.s" "index_005_r_bind.is";
connectAttr "wrist_r_bind.s" "pinkyCup_r_bind.is";
connectAttr "pinkyCup_r_bind.s" "pinky_001_r_bind.is";
connectAttr "pinky_001_r_bind.s" "pinky_002_r_bind.is";
connectAttr "pinky_002_r_bind.s" "pinky_003_r_bind.is";
connectAttr "pinky_003_r_bind.s" "pinky_004_r_bind.is";
connectAttr "pinky_004_r_bind.s" "pinky_005_r_bind.is";
connectAttr "wrist_r_bind.s" "thumbCup_r_bind.is";
connectAttr "thumbCup_r_bind.s" "thumb_001_r_bind.is";
connectAttr "thumb_001_r_bind.s" "thumb_002_r_bind.is";
connectAttr "thumb_002_r_bind.s" "thumb_003_r_bind.is";
connectAttr "thumb_003_r_bind.s" "thumb_004_r_bind.is";
connectAttr "wrist_r_bind.s" "wristTwist_r_bind.is";
connectAttr "clavicle_r_bind.s" "shoulderNoTwist_r_bind.is";
connectAttr "hips_bind.s" "pelvis_l_bind.is";
connectAttr "pelvis_l_bind.s" "thigh_l_bind.is";
connectAttr "thigh_l_bind.s" "knee_l_bind.is";
connectAttr "knee_l_bind.s" "ankle_l_bind.is";
connectAttr "ankle_l_bind.s" "ball_l_bind.is";
connectAttr "ball_l_bind.s" "toe_l_bind.is";
connectAttr "ankle_l_bind.s" "ankleTwist_l_bind.is";
connectAttr "ankleTwist_l_bind_aimConstraint1.crx" "ankleTwist_l_bind.rx";
connectAttr "ankleTwist_l_bind_aimConstraint1.cry" "ankleTwist_l_bind.ry";
connectAttr "ankleTwist_l_bind_aimConstraint1.crz" "ankleTwist_l_bind.rz";
connectAttr "ankleTwist_l_bind.pim" "ankleTwist_l_bind_aimConstraint1.cpim";
connectAttr "ankleTwist_l_bind.t" "ankleTwist_l_bind_aimConstraint1.ct";
connectAttr "ankleTwist_l_bind.rp" "ankleTwist_l_bind_aimConstraint1.crp";
connectAttr "ankleTwist_l_bind.rpt" "ankleTwist_l_bind_aimConstraint1.crt";
connectAttr "ankleTwist_l_bind.ro" "ankleTwist_l_bind_aimConstraint1.cro";
connectAttr "ankleTwist_l_bind.jo" "ankleTwist_l_bind_aimConstraint1.cjo";
connectAttr "ankleTwist_l_bind.is" "ankleTwist_l_bind_aimConstraint1.is";
connectAttr "knee_l_bind.t" "ankleTwist_l_bind_aimConstraint1.tg[0].tt";
connectAttr "knee_l_bind.rp" "ankleTwist_l_bind_aimConstraint1.tg[0].trp";
connectAttr "knee_l_bind.rpt" "ankleTwist_l_bind_aimConstraint1.tg[0].trt";
connectAttr "knee_l_bind.pm" "ankleTwist_l_bind_aimConstraint1.tg[0].tpm";
connectAttr "ankleTwist_l_bind_aimConstraint1.w0" "ankleTwist_l_bind_aimConstraint1.tg[0].tw"
		;
connectAttr "thigh_l_bind.jo" "thighNoTwist_l_bind.jo";
connectAttr "pelvis_l_bind.s" "thighNoTwist_l_bind.is";
connectAttr "thigh_l_bind.t" "thighNoTwist_l_bind.t";
connectAttr "thigh_l_bind.ro" "thighNoTwist_l_bind.ro";
connectAttr "thighNoTwist_l_bind_aimConstraint1.crx" "thighNoTwist_l_bind.rx";
connectAttr "thighNoTwist_l_bind_aimConstraint1.cry" "thighNoTwist_l_bind.ry";
connectAttr "thighNoTwist_l_bind_aimConstraint1.crz" "thighNoTwist_l_bind.rz";
connectAttr "thighNoTwist_l_bind.pim" "thighNoTwist_l_bind_aimConstraint1.cpim";
connectAttr "thighNoTwist_l_bind.t" "thighNoTwist_l_bind_aimConstraint1.ct";
connectAttr "thighNoTwist_l_bind.rp" "thighNoTwist_l_bind_aimConstraint1.crp";
connectAttr "thighNoTwist_l_bind.rpt" "thighNoTwist_l_bind_aimConstraint1.crt";
connectAttr "thighNoTwist_l_bind.ro" "thighNoTwist_l_bind_aimConstraint1.cro";
connectAttr "thighNoTwist_l_bind.jo" "thighNoTwist_l_bind_aimConstraint1.cjo";
connectAttr "thighNoTwist_l_bind.is" "thighNoTwist_l_bind_aimConstraint1.is";
connectAttr "knee_l_bind.t" "thighNoTwist_l_bind_aimConstraint1.tg[0].tt";
connectAttr "knee_l_bind.rp" "thighNoTwist_l_bind_aimConstraint1.tg[0].trp";
connectAttr "knee_l_bind.rpt" "thighNoTwist_l_bind_aimConstraint1.tg[0].trt";
connectAttr "knee_l_bind.pm" "thighNoTwist_l_bind_aimConstraint1.tg[0].tpm";
connectAttr "thighNoTwist_l_bind_aimConstraint1.w0" "thighNoTwist_l_bind_aimConstraint1.tg[0].tw"
		;
connectAttr "hips_bind.s" "pelvis_r_bind.is";
connectAttr "pelvis_r_bind.s" "thigh_r_bind.is";
connectAttr "thigh_r_bind.s" "knee_r_bind.is";
connectAttr "knee_r_bind.s" "ankle_r_bind.is";
connectAttr "ankle_r_bind.s" "ball_r_bind.is";
connectAttr "ball_r_bind.s" "toe_r_bind.is";
connectAttr "ankle_r_bind.s" "ankleTwist_r_bind.is";
connectAttr "ankleTwist_r_bind_aimConstraint1.crx" "ankleTwist_r_bind.rx";
connectAttr "ankleTwist_r_bind_aimConstraint1.cry" "ankleTwist_r_bind.ry";
connectAttr "ankleTwist_r_bind_aimConstraint1.crz" "ankleTwist_r_bind.rz";
connectAttr "ankleTwist_r_bind.pim" "ankleTwist_r_bind_aimConstraint1.cpim";
connectAttr "ankleTwist_r_bind.t" "ankleTwist_r_bind_aimConstraint1.ct";
connectAttr "ankleTwist_r_bind.rp" "ankleTwist_r_bind_aimConstraint1.crp";
connectAttr "ankleTwist_r_bind.rpt" "ankleTwist_r_bind_aimConstraint1.crt";
connectAttr "ankleTwist_r_bind.ro" "ankleTwist_r_bind_aimConstraint1.cro";
connectAttr "ankleTwist_r_bind.jo" "ankleTwist_r_bind_aimConstraint1.cjo";
connectAttr "ankleTwist_r_bind.is" "ankleTwist_r_bind_aimConstraint1.is";
connectAttr "knee_r_bind.t" "ankleTwist_r_bind_aimConstraint1.tg[0].tt";
connectAttr "knee_r_bind.rp" "ankleTwist_r_bind_aimConstraint1.tg[0].trp";
connectAttr "knee_r_bind.rpt" "ankleTwist_r_bind_aimConstraint1.tg[0].trt";
connectAttr "knee_r_bind.pm" "ankleTwist_r_bind_aimConstraint1.tg[0].tpm";
connectAttr "ankleTwist_r_bind_aimConstraint1.w0" "ankleTwist_r_bind_aimConstraint1.tg[0].tw"
		;
connectAttr "thigh_r_bind.jo" "thighNoTwist_r_bind.jo";
connectAttr "pelvis_r_bind.s" "thighNoTwist_r_bind.is";
connectAttr "thigh_r_bind.t" "thighNoTwist_r_bind.t";
connectAttr "thigh_r_bind.ro" "thighNoTwist_r_bind.ro";
connectAttr "thighNoTwist_r_bind_aimConstraint1.crx" "thighNoTwist_r_bind.rx";
connectAttr "thighNoTwist_r_bind_aimConstraint1.cry" "thighNoTwist_r_bind.ry";
connectAttr "thighNoTwist_r_bind_aimConstraint1.crz" "thighNoTwist_r_bind.rz";
connectAttr "thighNoTwist_r_bind.pim" "thighNoTwist_r_bind_aimConstraint1.cpim";
connectAttr "thighNoTwist_r_bind.t" "thighNoTwist_r_bind_aimConstraint1.ct";
connectAttr "thighNoTwist_r_bind.rp" "thighNoTwist_r_bind_aimConstraint1.crp";
connectAttr "thighNoTwist_r_bind.rpt" "thighNoTwist_r_bind_aimConstraint1.crt";
connectAttr "thighNoTwist_r_bind.ro" "thighNoTwist_r_bind_aimConstraint1.cro";
connectAttr "thighNoTwist_r_bind.jo" "thighNoTwist_r_bind_aimConstraint1.cjo";
connectAttr "thighNoTwist_r_bind.is" "thighNoTwist_r_bind_aimConstraint1.is";
connectAttr "knee_r_bind.t" "thighNoTwist_r_bind_aimConstraint1.tg[0].tt";
connectAttr "knee_r_bind.rp" "thighNoTwist_r_bind_aimConstraint1.tg[0].trp";
connectAttr "knee_r_bind.rpt" "thighNoTwist_r_bind_aimConstraint1.tg[0].trt";
connectAttr "knee_r_bind.pm" "thighNoTwist_r_bind_aimConstraint1.tg[0].tpm";
connectAttr "thighNoTwist_r_bind_aimConstraint1.w0" "thighNoTwist_r_bind_aimConstraint1.tg[0].tw"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "skeleton_renderLayerManager.rlmi[0]" "skeleton_defaultRenderLayer.rlid"
		;
connectAttr "skeleton_skeleton_renderLayerManager.rlmi[0]" "skeleton_skeleton_defaultRenderLayer.rlid"
		;
connectAttr "skeleton_skeleton_skeleton_renderLayerManager.rlmi[0]" "skeleton_skeleton_skeleton_defaultRenderLayer.rlid"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_renderLayerManager.rlmi[0]" "skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.rlid"
		;
connectAttr "biped_model_renderLayerManager.rlmi[0]" "biped_model_defaultRenderLayer.rlid"
		;
connectAttr "skeleton_renderLayerManager1.rlmi[0]" "skeleton_defaultRenderLayer1.rlid"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_renderLayerManager.rlmi[0]" "skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.rlid"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_renderLayerManager.rlmi[0]" "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.rlid"
		;
connectAttr "blink_curves_renderLayerManager.rlmi[0]" "blink_curves_defaultRenderLayer.rlid"
		;
connectAttr "middle_005_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[0].dn"
		;
connectAttr "neck_3_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[1].dn";
connectAttr "defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[2].dn"
		;
connectAttr "ring_003_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[3].dn"
		;
connectAttr "ring_004_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[4].dn"
		;
connectAttr "middle_004_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[5].dn"
		;
connectAttr "index_002_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[6].dn"
		;
connectAttr "index_005_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[7].dn"
		;
connectAttr "thumb_003_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[8].dn"
		;
connectAttr "neck_1_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[9].dn";
connectAttr "ring_003_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[10].dn"
		;
connectAttr "middle_003_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[11].dn"
		;
connectAttr "wrist_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[12].dn";
connectAttr "pinky_005_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[13].dn"
		;
connectAttr "middle_002_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[14].dn"
		;
connectAttr "index_001_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[15].dn"
		;
connectAttr "ring_002_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[16].dn"
		;
connectAttr "pinky_004_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[17].dn"
		;
connectAttr "index_004_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[18].dn"
		;
connectAttr "pinky_002_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[19].dn"
		;
connectAttr "thumbCup_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[20].dn"
		;
connectAttr "thumb_004_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[21].dn"
		;
connectAttr "middle_001_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[22].dn"
		;
connectAttr "thumb_001_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[23].dn"
		;
connectAttr "thumb_002_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[24].dn"
		;
connectAttr "shoulderNoTwist_l_bind_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[25].dn"
		;
connectAttr "neck_2_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[26].dn";
connectAttr "index_003_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[27].dn"
		;
connectAttr "ring_005_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[28].dn"
		;
connectAttr "neck_0_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[29].dn";
connectAttr "index_001_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[30].dn"
		;
connectAttr "pinkyCup_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[31].dn"
		;
connectAttr "skull_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[32].dn";
connectAttr "pinky_001_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[33].dn"
		;
connectAttr "pinky_003_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[34].dn"
		;
connectAttr "shoulderNoTwist_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[35].dn"
		;
connectAttr "eyeSocket_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[36].dn"
		;
connectAttr "wristTwist_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[37].dn"
		;
connectAttr "wristTwist_l_bind_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[38].dn"
		;
connectAttr "shoulder_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[39].dn"
		;
connectAttr "eyeSocket_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[40].dn"
		;
connectAttr "eye_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[41].dn";
connectAttr "elbow_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[42].dn";
connectAttr "ring_002_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[43].dn"
		;
connectAttr "clavicle_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[44].dn"
		;
connectAttr "ring_004_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[45].dn"
		;
connectAttr "ring_005_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[46].dn"
		;
connectAttr "eye_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[47].dn";
connectAttr "ring_001_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[48].dn"
		;
connectAttr "middle_001_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[49].dn"
		;
connectAttr "middle_002_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[50].dn"
		;
connectAttr "middle_003_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[51].dn"
		;
connectAttr "middle_004_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[52].dn"
		;
connectAttr "middle_005_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[53].dn"
		;
connectAttr "skeleton_skeleton_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[54].dn"
		;
connectAttr "thumb_004_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[55].dn"
		;
connectAttr "pinky_004_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[56].dn"
		;
connectAttr "ankleTwist_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[57].dn"
		;
connectAttr "knee_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[58].dn";
connectAttr "skeleton_defaultRenderLayer1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[59].dn"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[60].dn"
		;
connectAttr "toe_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[61].dn";
connectAttr "ankle_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[62].dn";
connectAttr "blink_curves_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[63].dn"
		;
connectAttr "pinkyCup_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[64].dn"
		;
connectAttr "index_004_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[65].dn"
		;
connectAttr "thumb_003_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[66].dn"
		;
connectAttr "thumb_002_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[67].dn"
		;
connectAttr "shoulderNoTwist_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[68].dn"
		;
connectAttr "wristTwist_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[69].dn"
		;
connectAttr "thumb_001_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[70].dn"
		;
connectAttr "knee_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[71].dn";
connectAttr "index_002_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[72].dn"
		;
connectAttr "index_003_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[73].dn"
		;
connectAttr "pinky_003_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[74].dn"
		;
connectAttr "pinky_005_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[75].dn"
		;
connectAttr "thigh_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[76].dn";
connectAttr "ankleTwist_l_bind_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[77].dn"
		;
connectAttr "thighNoTwist_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[78].dn"
		;
connectAttr "wristTwist_l_bind_aimConstraint2.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[79].dn"
		;
connectAttr "thighNoTwist_l_bind_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[80].dn"
		;
connectAttr "thigh_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[81].dn";
connectAttr "ankleTwist_r_bind_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[82].dn"
		;
connectAttr "thighNoTwist_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[83].dn"
		;
connectAttr "index_005_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[84].dn"
		;
connectAttr "thumbCup_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[85].dn"
		;
connectAttr "pelvis_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[86].dn";
connectAttr "ankle_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[87].dn";
connectAttr "toe_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[88].dn";
connectAttr "ankleTwist_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[89].dn"
		;
connectAttr "shoulderNoTwist_l_bind_aimConstraint2.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[90].dn"
		;
connectAttr "pinky_001_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[91].dn"
		;
connectAttr "ball_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[92].dn";
connectAttr "pelvis_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[93].dn";
connectAttr "ball_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[94].dn";
connectAttr "thighNoTwist_r_bind_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[95].dn"
		;
connectAttr "skeleton_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[96].dn"
		;
connectAttr "pinky_002_r_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[97].dn"
		;
connectAttr "skeleton_skeleton_skeleton_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[98].dn"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[99].dn"
		;
connectAttr "biped_model_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[100].dn"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[101].dn"
		;
connectAttr "bankIn_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[102].dn"
		;
connectAttr "ankle_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[103].dn"
		;
connectAttr "bankOut_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[104].dn"
		;
connectAttr "ball_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[105].dn";
connectAttr "toe_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[106].dn";
connectAttr "toeBend_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[107].dn"
		;
connectAttr "ballRoll_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[108].dn"
		;
connectAttr "ankle_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[109].dn"
		;
connectAttr "bankIn_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[110].dn"
		;
connectAttr "bankOut_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[111].dn"
		;
connectAttr "heel_l_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[112].dn";
connectAttr "shoulder_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[113].dn"
		;
connectAttr "heel_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[114].dn";
connectAttr "bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[115].dn";
connectAttr "ring_001_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[116].dn"
		;
connectAttr "hips_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[117].dn";
connectAttr "elbow_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[118].dn";
connectAttr "spine_4_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[119].dn";
connectAttr "toe_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[120].dn";
connectAttr "ball_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[121].dn";
connectAttr "toeBend_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[122].dn"
		;
connectAttr "spine_3_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[123].dn";
connectAttr "spine_5_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[124].dn";
connectAttr "ballRoll_r_pivot.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[125].dn"
		;
connectAttr "wrist_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[126].dn";
connectAttr "spine_0_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[127].dn";
connectAttr "spine_1_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[128].dn";
connectAttr "spine_2_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[129].dn";
connectAttr "chest_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[130].dn";
connectAttr "clavicle_l_bind.msg" "MayaNodeEditorSavedTabsInfo1.tgi[0].ni[131].dn"
		;
connectAttr "defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[0].dn"
		;
connectAttr "pinkyCup_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[1].dn"
		;
connectAttr "heel_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[2].dn"
		;
connectAttr "ring_002_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[3].dn"
		;
connectAttr "toe_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[4].dn"
		;
connectAttr "toeBend_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[5].dn"
		;
connectAttr "ballRoll_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[6].dn"
		;
connectAttr "ring_001_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[7].dn"
		;
connectAttr "middle_001_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[8].dn"
		;
connectAttr "middle_005_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[9].dn"
		;
connectAttr "index_003_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[10].dn"
		;
connectAttr "shoulder_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[11].dn"
		;
connectAttr "ring_003_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[12].dn"
		;
connectAttr "bankOut_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[13].dn"
		;
connectAttr "ballRoll_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[14].dn"
		;
connectAttr "spine_1_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[15].dn"
		;
connectAttr "bankIn_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[16].dn"
		;
connectAttr "bankOut_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[17].dn"
		;
connectAttr "spine_3_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[18].dn"
		;
connectAttr "ankle_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[19].dn"
		;
connectAttr "clavicle_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[20].dn"
		;
connectAttr "spine_5_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[21].dn"
		;
connectAttr "toe_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[22].dn"
		;
connectAttr "ankle_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[23].dn"
		;
connectAttr "toeBend_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[24].dn"
		;
connectAttr "bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[25].dn"
		;
connectAttr "bankIn_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[26].dn"
		;
connectAttr "spine_0_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[27].dn"
		;
connectAttr "spine_2_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[28].dn"
		;
connectAttr "spine_4_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[29].dn"
		;
connectAttr "wrist_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[30].dn"
		;
connectAttr "ring_005_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[31].dn"
		;
connectAttr "middle_004_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[32].dn"
		;
connectAttr "hips_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[33].dn"
		;
connectAttr "chest_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[34].dn"
		;
connectAttr "index_001_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[35].dn"
		;
connectAttr "ball_l_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[36].dn"
		;
connectAttr "middle_003_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[37].dn"
		;
connectAttr "ball_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[38].dn"
		;
connectAttr "index_004_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[39].dn"
		;
connectAttr "index_005_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[40].dn"
		;
connectAttr "pinky_001_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[41].dn"
		;
connectAttr "pinky_003_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[42].dn"
		;
connectAttr "ring_004_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[43].dn"
		;
connectAttr "elbow_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[44].dn"
		;
connectAttr "middle_002_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[45].dn"
		;
connectAttr "pinky_004_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[46].dn"
		;
connectAttr "heel_r_pivot.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[47].dn"
		;
connectAttr "index_002_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[48].dn"
		;
connectAttr "thumbCup_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[49].dn"
		;
connectAttr "thumb_003_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[50].dn"
		;
connectAttr "pinky_002_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[51].dn"
		;
connectAttr "thumb_004_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[52].dn"
		;
connectAttr "thumb_001_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[53].dn"
		;
connectAttr "wristTwist_l_bind_aimConstraint1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[54].dn"
		;
connectAttr "shoulderNoTwist_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[55].dn"
		;
connectAttr "pinky_005_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[56].dn"
		;
connectAttr "neck_0_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[57].dn"
		;
connectAttr "shoulderNoTwist_l_bind_aimConstraint1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[58].dn"
		;
connectAttr "neck_1_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[59].dn"
		;
connectAttr "neck_2_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[60].dn"
		;
connectAttr "thumb_002_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[61].dn"
		;
connectAttr "wristTwist_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[62].dn"
		;
connectAttr "neck_3_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[63].dn"
		;
connectAttr "skull_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[64].dn"
		;
connectAttr "ring_001_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[65].dn"
		;
connectAttr "middle_005_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[66].dn"
		;
connectAttr "pinky_003_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[67].dn"
		;
connectAttr "eyeSocket_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[68].dn"
		;
connectAttr "eye_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[69].dn"
		;
connectAttr "elbow_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[70].dn"
		;
connectAttr "ring_002_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[71].dn"
		;
connectAttr "index_001_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[72].dn"
		;
connectAttr "shoulder_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[73].dn"
		;
connectAttr "index_003_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[74].dn"
		;
connectAttr "eye_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[75].dn"
		;
connectAttr "wrist_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[76].dn"
		;
connectAttr "index_005_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[77].dn"
		;
connectAttr "ring_004_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[78].dn"
		;
connectAttr "middle_001_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[79].dn"
		;
connectAttr "ring_005_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[80].dn"
		;
connectAttr "middle_002_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[81].dn"
		;
connectAttr "eyeSocket_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[82].dn"
		;
connectAttr "middle_004_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[83].dn"
		;
connectAttr "pinkyCup_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[84].dn"
		;
connectAttr "pinky_001_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[85].dn"
		;
connectAttr "pinky_002_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[86].dn"
		;
connectAttr "index_002_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[87].dn"
		;
connectAttr "clavicle_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[88].dn"
		;
connectAttr "ring_003_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[89].dn"
		;
connectAttr "middle_003_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[90].dn"
		;
connectAttr "index_004_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[91].dn"
		;
connectAttr "pinky_004_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[92].dn"
		;
connectAttr "pinky_005_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[93].dn"
		;
connectAttr "thumbCup_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[94].dn"
		;
connectAttr "thumb_001_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[95].dn"
		;
connectAttr "thumb_002_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[96].dn"
		;
connectAttr "thumb_003_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[97].dn"
		;
connectAttr "thumb_004_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[98].dn"
		;
connectAttr "wristTwist_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[99].dn"
		;
connectAttr "wristTwist_l_bind_aimConstraint2.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[100].dn"
		;
connectAttr "shoulderNoTwist_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[101].dn"
		;
connectAttr "shoulderNoTwist_l_bind_aimConstraint2.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[102].dn"
		;
connectAttr "thighNoTwist_r_bind_aimConstraint1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[103].dn"
		;
connectAttr "ankleTwist_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[104].dn"
		;
connectAttr "ankleTwist_r_bind_aimConstraint1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[105].dn"
		;
connectAttr "ball_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[106].dn"
		;
connectAttr "ankle_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[107].dn"
		;
connectAttr "pelvis_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[108].dn"
		;
connectAttr "thigh_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[109].dn"
		;
connectAttr "thighNoTwist_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[110].dn"
		;
connectAttr "toe_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[111].dn"
		;
connectAttr "skeleton_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[112].dn"
		;
connectAttr "knee_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[113].dn"
		;
connectAttr "pelvis_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[114].dn"
		;
connectAttr "thighNoTwist_l_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[115].dn"
		;
connectAttr "thighNoTwist_l_bind_aimConstraint1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[116].dn"
		;
connectAttr "skeleton_skeleton_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[117].dn"
		;
connectAttr "skeleton_defaultRenderLayer1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[118].dn"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[119].dn"
		;
connectAttr "thigh_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[120].dn"
		;
connectAttr "ankle_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[121].dn"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[122].dn"
		;
connectAttr "skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[123].dn"
		;
connectAttr "knee_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[124].dn"
		;
connectAttr "skeleton_skeleton_skeleton_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[125].dn"
		;
connectAttr "blink_curves_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[126].dn"
		;
connectAttr "toe_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[127].dn"
		;
connectAttr "ankleTwist_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[128].dn"
		;
connectAttr "ball_r_bind.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[129].dn"
		;
connectAttr "biped_model_defaultRenderLayer.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[130].dn"
		;
connectAttr "ankleTwist_l_bind_aimConstraint1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo1.tgi[0].ni[131].dn"
		;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "skeleton_defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "skeleton_skeleton_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "skeleton_skeleton_skeleton_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "biped_model_defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "skeleton_defaultRenderLayer1.msg" ":defaultRenderingList1.r" -na;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "skeleton_skeleton_skeleton_skeleton_skeleton_skeleton_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "blink_curves_defaultRenderLayer.msg" ":defaultRenderingList1.r" -na
		;
// End of skeleton.ma
