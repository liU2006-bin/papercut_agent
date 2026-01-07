import json
data = {
    "knowledge_base": {
        "name": "陕北剪纸纹样知识库",
        "version": "1.0",
        "description": "基于《陕北剪纸的分布与特点》论文构建的专业知识库，支持剪纸纹样识别、寓意解读和创意组合建议",
        "created_at": "2024-01-15",

        "regions": [
            {
                "id": "region_yanan_south",
                "name": "延安南部",
                "counties": ["富县", "洛川", "黄陵", "宜川"],
                "cultural_features": "关中文化向陕北过渡地带，说秦话、唱秦腔，较多保留关中古老民俗",
                "artistic_style": "秀丽工细，格调明快，注重文化内涵和造型变化",
                "representative_techniques": ["单色剪纸", "拼贴剪纸", "衬色剪纸", "熏样法"],
                "color_preferences": ["红色为主", "多色拼贴"],
                "taboos": ["无明显禁忌"]
            },
            {
                "id": "region_yansui",
                "name": "延绥地区",
                "counties": ["宝塔区", "甘泉", "安塞", "志丹", "子长", "延川", "延长", "榆阳区", "绥德", "米脂", "子洲", "清涧", "吴堡", "佳县", "横山"],
                "cultural_features": "陕北剪纸主体，自我表现艺术，原始文化遗存丰富",
                "artistic_style": "简练朴实，注重对称美、装饰美，原创性强",
                "representative_techniques": ["信手剪", "不画样儿", "对称剪法"],
                "color_preferences": ["红色", "黄色（黄表纸，象征黄帝）"],
                "taboos": ["忌讳剪人、贴人", "忌黑色窗花", "忌剪骆驼（认为会败家）"]
            },
            {
                "id": "region_yulin_northwest",
                "name": "榆林西北部（三边地区）",
                "counties": ["靖边", "定边", "安边", "横山北部", "榆阳", "神木", "府谷", "吴起北部"],
                "cultural_features": "汉民族与北方游牧民族文化融合，江南文化与陕北文化交融",
                "artistic_style": "粗犷中见秀美，古拙中见细腻，线条纤细入微",
                "representative_techniques": ["细毛剪法", "针眼掏孔", "发丝线条"],
                "color_preferences": ["不忌黑色", "多色并用"],
                "taboos": ["无黑色禁忌", "骆驼为吉祥物（与延绥相反）"]
            }
        ],

        "patterns": [
            {
                "id": "pattern_001",
                "name": "双雁喜花",
                "aliases": ["双雁纹", "大雁喜花"],
                "region_id": "region_yanan_south",
                "appearance_description": "由街首交尾的两只大雁组成，或左右对称的两个雁字组成，周围装饰牡丹、莲花等吉祥纹饰",
                "symbolism": ["夫妻忠贞", "婚姻美满", "白头偕老"],
                "cultural_background": "源于西周婚礼习俗，《周礼·婚经》记载纳彩、请期等婚礼环节皆用雁。大雁终生一夫一妻，如一方死亡，另一方不再配偶",
                "usage_scenarios": ["婚庆正堂中心", "婚礼仪式", "新娘嫁妆"],
                "ritual_significance": "新郎新娘需向双雁行三拜礼，然后夫妻对拜",
                "confidence_levels": {
                    "recognition": 95,
                    "interpretation": 90
                },
                "related_patterns": ["pattern_002"],
                "image_urls": [
                    "images/1.png",
                    "images/2.png"
                ]
            },
            {
                "id": "pattern_002",
                "name": "鱼纹",
                "aliases": ["鱼变娃", "人首鱼身"],
                "region_id": "region_yanan_south",
                "appearance_description": "鱼形图案，常与人首组合成人首鱼身，或与莲花组合",
                "symbolism": ["年年有余", "多子多福", "阴阳结合", "送子功能"],
                "cultural_background": "鱼喻阴喻地，象征女性生殖力。鱼钻莲图案反映生育过程和古老生殖观念",
                "usage_scenarios": ["婚俗喜花", "窗花", "墙花"],
                "ritual_significance": "象征阴阳结合、生命繁衍",
                "confidence_levels": {
                    "recognition": 93,
                    "interpretation": 85
                },
                "image_urls": [
                    "images/3.jpg",
                    "images/4.png"
                ]
            },
            {
                "id": "pattern_003",
                "name": "葫芦纹",
                "aliases": ["定帐葫芦", "红葫芦团花"],
                "region_id": "region_yansui",
                "appearance_description": "葫芦形状，常为对称团花样式",
                "symbolism": ["辟邪禳灾", "祈予纳福", "生命孕育", "混沌多子"],
                "cultural_background": "远古人类始祖伏羲、女娲在葫芦中逃过洪水，后繁衍人类。古代婚礼'合卺'即用葫芦瓢",
                "usage_scenarios": ["天窗正中", "婚房喜花", "端午节", "生育报喜"],
                "ritual_significance": "春节贴葫芦避灾，结婚贴葫芦祈子，生男孩贴葫芦报喜辟邪",
                "confidence_levels": {
                    "recognition": 91,
                    "interpretation": 87
                },
                "image_urls": [
                    "images/5.jpg",
                    "images/6.jpg"
                ]
            },
            {
                "id": "pattern_004",
                "name": "抓髻娃娃",
                "aliases": ["喜娃娃", "催生娃娃", "瓜子娃娃"],
                "region_id": "region_yansui",
                "appearance_description": "手拉手、八叉腿的娃娃形象，或一手抓鸡一手抓兔，或双手抓鸡脚踩莲花",
                "symbolism": ["喜神", "送子", "辟邪", "护生", "防瘟疫"],
                "cultural_background": "可能是商代文化遗存，与故宫博物院商代青玉女佩相似。民间认为是保护神，不是凡人",
                "usage_scenarios": ["门楣装饰", "婚俗窗花", "端午节", "坐帐花"],
                "ritual_significance": "守门防盗、防瘟疫、送子求福。忌讳剪人但不忌讳贴抓髻娃娃",
                "confidence_levels": {
                    "recognition": 96,
                    "interpretation": 92
                },
                "subtypes": [
                    {
                        "name": "瓜子娃娃",
                        "description": "身和四肢用纸剪，头用南瓜子代替，画上面部五官"
                    },
                    {
                        "name": "坐帐娃娃",
                        "description": "踩莲花、配石榴桃笙等吉祥符号，用于婚床装饰"
                    }
                ],
                "image_urls": [
                    "images/7.png",
                    "images/8.png"
                ]
            },
            {
                "id": "pattern_005",
                "name": "虎纹",
                "aliases": ["文虎", "龙虎", "送子虎"],
                "region_id": "region_yansui",
                "appearance_description": "虎形图案，有的头上有'王'字，有的无'王'字称龙虎",
                "symbolism": ["辟邪纳福", "镇宅平安", "护生送子", "增寿"],
                "cultural_background": "虎文化可溯至6000年前新石器时代，虎图腾逐渐融入民间信仰",
                "usage_scenarios": ["春节门神", "室内镇宅", "小孩护生", "端午节镇五毒"],
                "ritual_significance": "虎头上'王'字是通天符号，有王字的虎是保护神；龙虎更凶猛主要用于护生",
                "confidence_levels": {
                    "recognition": 95,
                    "interpretation": 89
                },
                "image_urls": [
                    "images/9.jpg"
                ]
            },
            {
                "id": "pattern_006",
                "name": "狮纹",
                "aliases": ["文狮子", "武狮子", "青狮"],
                "region_id": "region_yansui",
                "appearance_description": "狮子图案，文狮子用花草装饰，武狮子用锯齿纹表现凶猛",
                "symbolism": ["镇妖辟邪", "爱情象征", "事事如意", "扫除晦气"],
                "cultural_background": "汉代传入中国，随佛教传播融入民俗。青狮谐音'情狮'象征爱情",
                "usage_scenarios": ["窗花", "婚俗喜花", "驱邪治病", "镇宅"],
                "ritual_significance": "用于家中不顺、男人寿不长时扫晦气；娃娃生病时驱'瘫甲子'鬼",
                "confidence_levels": {
                    "recognition": 93,
                    "interpretation": 86
                },
                "image_urls": [
                    "images/10.jpg",
                    "images/11.jpg"
                ]
            },
            {
                "id": "pattern_007",
                "name": "鸡衔鱼",
                "aliases": ["鸟衔鱼", "鹭鸶衔鱼"],
                "region_id": "region_yansui",
                "appearance_description": "鸡或鸟衔着鱼的图案，风格古朴简洁",
                "symbolism": ["天地交合", "男女结合", "子孙繁衍", "阴阳相合"],
                "cultural_background": "源于仰韶文化彩陶'鸟衔鱼'纹饰，体现原始先民生殖崇拜",
                "usage_scenarios": ["窗花", "墙花", "传统装饰"],
                "ritual_significance": "鸡（鸟）喻阳喻天，鱼喻阴喻地，象征天地交合繁衍后代",
                "confidence_levels": {
                    "recognition": 90,
                    "interpretation": 84
                },
                "image_urls": [
                    "images/12.png",
                    "images/13.jpg",
                    "images/14.jpg"
                ]
            },
            {
                "id": "pattern_008",
                "name": "石榴纹",
                "aliases": ["石榴坐牡丹", "石榴花"],
                "regions": ["region_yanan_south", "region_yansui"],
                "appearance_description": "石榴果实或石榴花图案，常与牡丹、莲花等组合",
                "symbolism": ["多子多福", "家族兴旺", "吉祥富贵"],
                "cultural_background": "传统吉祥图案，石榴籽多象征子孙繁多",
                "usage_scenarios": ["婚俗喜花", "刺绣花样", "窗花"],
                "ritual_significance": "常用于婚礼祝福新人多子多孙",
                "confidence_levels": {
                    "recognition": 92,
                    "interpretation": 88
                },
                "image_urls": [
                    "images/15.png"
                ]
            },
            {
                "id": "pattern_009",
                "name": "牡丹纹",
                "aliases": ["富贵牡丹", "牡丹富贵"],
                "regions": ["region_yanan_south", "region_yansui"],
                "appearance_description": "牡丹花图案，富丽堂皇",
                "symbolism": ["富贵吉祥", "幸福美满", "女性美丽"],
                "cultural_background": "传统名花，象征富贵荣华",
                "usage_scenarios": ["喜花", "刺绣花样", "装饰图案"],
                "ritual_significance": "常用于婚庆祝福富贵吉祥",
                "confidence_levels": {
                    "recognition": 96,
                    "interpretation": 90
                },
                "image_urls": [
                    "images/16.png",
                    "images/17.png"
                ]
            },
            {
                "id": "pattern_010",
                "name": "莲花纹",
                "aliases": ["莲花", "荷花"],
                "regions": ["region_yanan_south", "region_yansui"],
                "appearance_description": "莲花图案，常与鱼、蛙等组合",
                "symbolism": ["纯洁高雅", "多子多福", "阴阳结合"],
                "cultural_background": "佛教圣花，民间喻阴喻女，象征纯洁",
                "usage_scenarios": ["婚俗喜花", "刺绣花样", "宗教装饰"],
                "ritual_significance": "莲花喻女阴，鱼钻莲象征男女结合生育",
                "confidence_levels": {
                    "recognition": 94,
                    "interpretation": 87
                },
                "image_urls": [
                    "images/18.png",
                    "images/19.jpg"
                ]
            },
            {
                "id": "pattern_011",
                "name": "五福捧寿",
                "aliases": ["五福临门", "寿字蝙蝠"],
                "region_ids": ["region_yanan_south", "region_yansui"],
                "appearance_description": "中央为寿字或仙桃，周围环绕五只蝙蝠的对称图案",
                "symbolism": ["长寿安康", "福气盈门", "吉祥圆满"],
                "cultural_background": "源自《尚书·洪范》'五福'概念（寿、富、康宁、攸好德、考终命），蝙蝠谐音'福'",
                "usage_scenarios": ["寿诞庆典", "老人居室", "春节装饰"],
                "ritual_significance": "用于祝寿场合，祈求老人健康长寿，福气绵长",
                "confidence_levels": {"recognition": 97, "interpretation": 95},
                "image_urls": ["images/22.png","images/23.png"]
            },

            {
                "id": "pattern_012",
                "name": "喜鹊登梅",
                "aliases": ["喜上眉梢", "鹊梅图"],
                "region_ids": ["region_yanan_south", "region_yulin_northwest"],
                "appearance_description": "喜鹊站立在梅枝上的图案，常配以花朵",
                "symbolism": ["喜事临门", "好运将至", "坚韧不拔", "喜上眉梢"],
                "cultural_background": "中国传统吉祥图案，'梅'谐音'眉'，喜鹊报喜传说流传千年",
                "usage_scenarios": ["婚礼喜花", "春节窗花", "乔迁贺礼"],
                "ritual_significance": "象征喜事即将到来，常用于新婚、升学、升迁等喜庆场合",
                "confidence_levels": {"recognition": 96, "interpretation": 92},
                "image_urls": ["images/24.png"]
            },
            {
                "id": "pattern_013",
                "name": "碗架云子",
                "aliases": ["板架云子", "碗架花"],
                "region_id": "region_yanan_south",
                "appearance_description": "形似门笺，25cm×15cm大小，花草或动物图案",
                "symbolism": ["家庭美满", "生活富足", "美观装饰"],
                "cultural_background": "关中剪纸古老纹饰的延续",
                "usage_scenarios": ["碗架装饰", "居室美化"],
                "ritual_significance": "用熏样法制作，黑白样式在碗架上呈二方连续排列",
                "confidence_levels": {
                    "recognition": 88,
                    "interpretation": 83
                },
                "image_urls": ["images/25.png", "images/26.png"]
            },
            {
                "id": "pattern_014",
                "name": "帽子花",
                "aliases": ["祭祀花", "老影花"],
                "region_id": "region_yanan_south",
                "appearance_description": "大幅装饰图案，像戏台幕帐",
                "symbolism": ["祭祀祖先", "家族传承", "肃穆庄重"],
                "cultural_background": "春节祭祀祖先'拜老影'的装饰",
                "usage_scenarios": ["祭祀厅堂", "祖先牌位两侧"],
                "ritual_significance": "烘托祭祀厅堂的庄重美观",
                "confidence_levels": {
                    "recognition": 87,
                    "interpretation": 81
                },
                "image_urls": [
                    "images/29.png",
                    "images/30.png"
                ]
            },
            {
                "id": "pattern_015",
                "name": "龙纹",
                "aliases": ["龙形纹饰", "盘龙纹"],
                "region_id": "region_yanan_south",
                "appearance_description": "传统龙形图案，形态威严生动，常见于器物、建筑与织物之上",
                "symbolism": ["权力尊贵", "祥瑞护佑", "力量智慧", "吉祥腾达"],
                "cultural_background": "中华文明核心图腾之一，象征皇权、天意与民族精神，贯穿历代艺术",
                "usage_scenarios": ["仪式庆典", "建筑装饰", "器物纹饰", "服饰织绣"],
                "ritual_significance": "常用于重大礼仪场合，代表权威与吉祥，布局讲究对称或环绕，体现天人合一观念",
                "confidence_levels": {
                    "recognition": 96,
                    "interpretation": 94
                },
                "image_urls": [
                    "images/20.jpg",
                    "images/21.png"
                ]
            },
            {
                "id": "pattern_016",
                "name": "连年有余",
                "aliases": ["莲花鲤鱼", "鱼戏莲"],
                "region_ids": ["region_yanan_south", "region_yansui", "region_yulin_northwest"],
                "appearance_description": "莲花与鲤鱼组合的图案，鱼在莲间游动",
                "symbolism": ["年年富足", "吉祥如意", "生活美满", "学业有成"],
                "cultural_background": "传统吉祥图案，'莲'谐音'连'，'鱼'谐音'余'，寓意延续不断",
                "usage_scenarios": ["春节装饰", "年画", "家居装饰", "商业场所"],
                "ritual_significance": "祈求来年丰收富裕，生活安康，是春节最常见纹样之一",
                "confidence_levels": {"recognition": 98, "interpretation": 96},
                "image_urls": ["images/27.png", "images/28.png", "images/29.png"]
            }
        ],
            
        "pattern_combinations": [
            {
                "combination_id": "combo_001",
                "name": "鱼莲组合",
                "patterns": ["pattern_002", "pattern_010"],
                "combined_name": "鱼钻莲/连年有余",
                "symbolism": ["夫妻恩爱", "连年有余", "多子多福", "阴阳和谐"],
                "design_suggestions": [
                    "鱼在莲叶下游动，嘴部靠近莲蓬",
                    "莲花盛开，鱼身环绕花茎",
                    "多条小鱼围绕一朵大莲花",
                    "可加入水波纹增强动感"
                ],
                "usage_scenarios": ["婚庆喜花", "春节窗花", "新房装饰"],
                "regional_variations": {
                    "延安南部": "鱼身细腻，莲花造型工整",
                    "延绥地区": "造型简练，强调对称",
                    "三边地区": "线条纤细，细节丰富"
                },
                "confidence_levels": {
                    "recognition": 94,
                    "interpretation": 91
                }
            },
            {
                "combination_id": "combo_002",
                "name": "五福捧寿组合",
                "patterns": ["pattern_011"],
                "combined_name": "五福捧寿",
                "symbolism": ["长寿安康", "福气盈门", "吉祥圆满"],
                "design_suggestions": [
                    "中央为大寿字，周围环绕五只蝙蝠",
                    "蝙蝠翅膀展开，呈现飞翔姿态",
                    "可添加祥云纹增强吉祥氛围",
                    "采用红色为主色调，象征喜庆"
                ],
                "usage_scenarios": ["寿诞庆典", "老人居室", "春节装饰"],
                "regional_variations": {
                    "延安南部": "造型秀丽工细，蝙蝠形态生动",
                    "延绥地区": "造型简练，强调对称美"
                },
                "confidence_levels": {
                    "recognition": 97,
                    "interpretation": 95
                }
            },
            {
                "combination_id": "combo_003",
                "name": "抓髻娃娃组合",
                "patterns": ["pattern_004", "pattern_008", "pattern_009"],
                "combined_name": "抓髻娃娃坐帐花",
                "symbolism": ["送子祈福", "辟邪护生", "多子多福"],
                "design_suggestions": [
                    "抓髻娃娃脚踩莲花，手举石榴",
                    "娃娃周围装饰牡丹、莲花、贯钱等",
                    "可设计双人抓髻娃娃，象征夫妻",
                    "背景可添加云勾、花卉纹饰"
                ],
                "usage_scenarios": ["婚床坐帐", "新房窗花", "求子祈福"],
                "regional_variations": {
                    "延绥地区": "娃娃造型古朴，装饰简洁",
                    "延安南部": "娃娃服饰细致，装饰繁复"
                },
                "confidence_levels": {
                    "recognition": 96,
                    "interpretation": 93
                }
            },
            {
                "combination_id": "combo_004",
                "name": "鸡鱼组合",
                "patterns": ["pattern_007"],
                "combined_name": "鸡衔鱼",
                "symbolism": ["天地交合", "阴阳结合", "子孙繁衍"],
                "design_suggestions": [
                    "鸡（鸟）衔着鱼的颈部或尾部",
                    "鸡翅展开，鱼身弯曲呈挣扎状",
                    "可添加太阳、云纹强调'天'的意象",
                    "可添加水波纹强调'地'的意象"
                ],
                "usage_scenarios": ["传统窗花", "文化装饰", "学术研究样本"],
                "regional_variations": {
                    "延绥地区": "风格古朴，有汉画像石特点",
                    "延安南部": "造型工细，装饰性强"
                },
                "confidence_levels": {
                    "recognition": 91,
                    "interpretation": 86
                }
            },
            {
                "combination_id": "combo_005",
                "name": "葫芦组合",
                "patterns": ["pattern_003", "pattern_004", "pattern_008"],
                "combined_name": "葫芦送子",
                "symbolism": ["辟邪纳福", "多子多孙", "生命孕育"],
                "design_suggestions": [
                    "大葫芦中心装饰娃娃或石榴",
                    "葫芦周围装饰莲花、牡丹",
                    "葫芦可设计为开口状，内有娃娃",
                    "可添加蔓藤缠绕，象征生命延续"
                ],
                "usage_scenarios": ["婚房喜花", "天窗装饰", "生育祈福"],
                "regional_variations": {
                    "延绥地区": "葫芦造型朴实，纹饰简洁",
                    "延安南部": "葫芦装饰繁复，色彩丰富"
                },
                "confidence_levels": {
                    "recognition": 92,
                    "interpretation": 88
                }
            },
            {
                "combination_id": "combo_006",
                "name": "双雁喜花组合",
                "patterns": ["pattern_001"],
                "combined_name": "双雁喜花",
                "symbolism": ["夫妻忠贞", "婚姻美满", "白头偕老"],
                "design_suggestions": [
                    "双雁交颈相对，对称布局",
                    "周围装饰牡丹、莲花等吉祥纹饰",
                    "可添加祥云纹增强喜庆氛围",
                    "采用红色为主色调，象征喜庆"
                ],
                "usage_scenarios": ["婚庆正堂中心", "婚礼仪式", "新娘嫁妆"],
                "regional_variations": {
                    "延安南部": "造型秀丽工细，格调明快",
                    "延绥地区": "造型简练，注重对称美"
                },
                "confidence_levels": {
                    "recognition": 95,
                    "interpretation": 90
                }
            },
            {
                "combination_id": "combo_007",
                "name": "龙虎组合",
                "patterns": ["pattern_005", "pattern_015"],
                "combined_name": "龙虎呈祥",
                "symbolism": ["权力尊贵", "祥瑞护佑", "镇宅辟邪", "吉祥腾达"],
                "design_suggestions": [
                    "龙在左，虎在右，呈对称布局",
                    "龙形威严，虎形勇猛",
                    "周围装饰云纹、火纹",
                    "可用于大型装饰，象征权威"
                ],
                "usage_scenarios": ["仪式庆典", "建筑装饰", "器物纹饰"],
                "regional_variations": {
                    "延安南部": "造型工整，细节丰富",
                    "延绥地区": "造型简练，线条粗犷"
                },
                "confidence_levels": {
                    "recognition": 93,
                    "interpretation": 90
                }
            },
            {
                "combination_id": "combo_008",
                "name": "喜鹊登梅组合",
                "patterns": ["pattern_012"],
                "combined_name": "喜鹊登梅",
                "symbolism": ["喜事临门", "好运将至", "坚韧不拔", "喜上眉梢"],
                "design_suggestions": [
                    "喜鹊站立在梅枝上，呈鸣叫姿态",
                    "梅枝上有盛开的梅花和花苞",
                    "可添加竹叶、松枝等元素增强画面",
                    "采用红色为主色调，象征喜庆"
                ],
                "usage_scenarios": ["婚礼喜花", "春节窗花", "乔迁贺礼"],
                "regional_variations": {
                    "延安南部": "造型秀丽工细，细节丰富",
                    "三边地区": "线条纤细，装饰繁复"
                },
                "confidence_levels": {
                    "recognition": 96,
                    "interpretation": 92
                }
            },
            {
                "combination_id": "combo_009",
                "name": "连年有余组合",
                "patterns": ["pattern_016"],
                "combined_name": "连年有余",
                "symbolism": ["年年富足", "吉祥如意", "生活美满", "学业有成"],
                "design_suggestions": [
                    "莲花盛开，鱼在莲间游动",
                    "鱼身装饰鳞片，形态生动",
                    "可添加水波纹增强动感",
                    "采用红色为主色调，象征喜庆"
                ],
                "usage_scenarios": ["春节装饰", "年画", "家居装饰", "商业场所"],
                "regional_variations": {
                    "延安南部": "造型秀丽工细，色彩丰富",
                    "延绥地区": "造型简练，强调对称美",
                    "三边地区": "线条纤细，细节丰富"
                },
                "confidence_levels": {
                    "recognition": 98,
                    "interpretation": 96
                }
            }
        ],

        "pattern_recognition_features": {
            "feature_categories": [
                {
                    "category": "动物纹样",
                    "patterns": ["pattern_001", "pattern_002", "pattern_005", "pattern_006", "pattern_007", "pattern_012", "pattern_015", "pattern_016"],
                    "识别特征": [
                        "双雁：交颈姿态，对称布局，常配花草",
                        "鱼纹：鳞片明显，尾部摆动，常与莲组合",
                        "虎纹：头有'王'字，尾巴上扬，威严凶猛",
                        "狮纹：卷毛装饰，大眼阔口，文武有别",
                        "喜鹊：翘尾展翅，常立梅枝",
                        "龙纹：蛇身鹿角，鹰爪鱼鳞，威严生动"
                    ]
                },
                {
                    "category": "植物纹样",
                    "patterns": ["pattern_003", "pattern_008", "pattern_009", "pattern_010"],
                    "识别特征": [
                        "葫芦：对称造型，腰部收缩，常配蔓藤",
                        "石榴：开口露籽，顶部花萼，象征多子",
                        "牡丹：花瓣繁复，富贵饱满，层叠华丽",
                        "莲花：花瓣尖长，莲蓬明显，纯洁高雅",
                        "梅花：五瓣花朵，枝干苍劲，寒冬绽放"
                    ]
                },
                {
                    "category": "人物纹样",
                    "patterns": ["pattern_004"],
                    "识别特征": [
                        "抓髻娃娃：双臂平举，双腿叉开，头有发髻，造型古朴",
                        "瓜子娃娃：南瓜子头部，纸剪身体，简单可爱"
                    ]
                },
                {
                    "category": "吉祥组合纹样",
                    "patterns": ["pattern_011", "pattern_013", "pattern_014", "pattern_016"],
                    "识别特征": [
                        "五福捧寿：中央寿字，五蝠环绕，对称布局",
                        "碗架云子：长方形，镂空装饰，连续排列",
                        "帽子花：大幅幕帐式，祭祀用，庄重繁复",
                        "连年有余：莲花鲤鱼组合，'莲'谐'连'，'鱼'谐'余'"
                    ]
                }
            ]
        },

        "qa_templates": [
            {
                "question_type": "纹样识别",
                "template": "识别结果为'[pattern_name]'，置信度[confidence]%。[pattern_name]在[region_name]剪纸中[symbolism_summary]...",
                "example": "识别结果为'鱼纹'，置信度92%。鱼纹在安塞剪纸中象征年年有余、多子多福..."
            },
            {
                "question_type": "寓意解读",
                "template": "[pattern_name]在[region_name]地区主要寓意：[symbolism_list]。文化背景：[cultural_background_summary]。常用于[usage_scenarios]场景。",
                "example": "鱼纹在延绥剪纸中主要寓意：年年有余、多子多福、阴阳结合。文化背景：源于仰韶文化，鱼喻阴喻地，象征女性生殖力。常用于婚俗喜花、窗花等场景。"
            },
            {
                "question_type": "组合建议",
                "template": "[pattern1]和[pattern2]组合寓意'[combined_symbolism]'，建议设计为[design_suggestion]。这种组合在[region_name]地区常见，常用于[usage]场景。",
                "example": "鱼纹和莲花纹组合寓意'连年有余'，建议设计为鱼在莲叶下游动，嘴部靠近莲蓬。这种组合在延安南部地区常见，常用于婚庆喜花场景。"
            },
            {
                "question_type": "地域差异",
                "template": "[pattern_name]在不同地区有不同特点：[regional_comparison]。文化差异原因：[cultural_reason]。",
                "example": "葫芦纹在延绥地区用于辟邪求子，在三边地区受蒙古文化影响寓意略有不同..."
            }
        ],

        "training_data": {
            "recognition_samples": [
                {
                    "image_description": "对称的双鸟交颈图案，周围有牡丹装饰",
                    "correct_pattern": "pattern_001",
                    "confidence": 95,
                    "region_hint": "延安南部"
                },
                {
                    "image_description": "五只蝙蝠环绕寿字的对称图案",
                    "correct_pattern": "pattern_011",
                    "confidence": 97,
                    "region_hint": "延安南部"
                },
                {
                    "image_description": "喜鹊站在梅花枝头，姿态生动",
                    "correct_pattern": "pattern_012",
                    "confidence": 96,
                    "region_hint": "榆林西北部"
                },
                {
                    "image_description": "莲花与鲤鱼组合，鱼在莲间游动",
                    "correct_pattern": "pattern_016",
                    "confidence": 98,
                    "region_hint": "普遍"
                }
            ],
            "interpretation_samples": [
                {
                    "pattern": "pattern_011",
                    "question": "五福捧寿有什么寓意？",
                    "answer": "五福捧寿纹样中，五只蝙蝠代表'五福'：长寿、富贵、康宁、好德、善终。寿字或仙桃象征长寿。整体寓意福寿双全，吉祥圆满。常用于老人寿诞，表达对长寿安康的祝愿。"
                },
                {
                    "pattern": "pattern_012",
                    "question": "喜鹊登梅为什么象征喜事？",
                    "answer": "喜鹊登梅中，喜鹊自古被视为报喜之鸟，'梅'谐音'眉'，寓意'喜上眉梢'。梅花寒冬绽放，象征坚韧不拔。组合寓意喜事即将到来，且经过艰难终得美好结果。常用于婚礼、升学等喜庆场合。"
                },
                {
                    "pattern": "pattern_016",
                    "question": "连年有余的深层含义是什么？",
                    "answer": "连年有余纹样中，'莲'谐音'连'，'鱼'谐音'余'，寓意每年都有富余。深层上，莲花象征纯洁、多子，鱼象征繁衍、富足。组合表达对连续丰收、生活富足、子孙繁衍的多重期盼，是中国最经典的吉祥图案之一。"
                }
            ]
        },

        "metadata": {
            "source_paper": "《陕北剪纸的分布与特点》陈山桥，咸阳师范学院学报2018年第1期",
            "extraction_method": "人工精炼提取与常见纹样补充",
            "coverage": "覆盖陕北主要纹样，补充常见吉祥图案",
            "applications": ["剪纸识别", "寓意解读", "设计建议", "文化教育", "文创开发"],
            "update_notes": "1. 替换不常见纹样为经典吉祥纹样 2. 统一字段格式 3. 优化纹样组合设计 4. 增加纹样覆盖范围"
        }
    }
}
