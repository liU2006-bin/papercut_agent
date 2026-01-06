import json
new_data = {
  "metadata": {
    "title": "安塞剪纸非遗文化知识库",
    "version": "2.0.0",
    "created_date": "2024-01-20",
    "last_updated": "2024-01-20",
    "description": "安塞剪纸全领域知识结构化数据库，包含纹样、技法、传承人、民俗等8大模块",
    "language": "zh-CN",
    "author": "安塞剪纸保护中心",
    "record_count": 348
  },

  "history_timeline": [
    {
      "period": "汉代",
      "stage": "起源期",
      "characteristics": ["祭祀用品", "简单几何纹样", "随葬品装饰"],
      "evidence": ["墓葬考古发现"],
      "significance": "剪纸艺术萌芽"
    },
    {
      "period": "魏晋",
      "stage": "初步发展",
      "characteristics": ["佛教影响", "莲花纹样出现", "宗教题材"],
      "evidence": ["敦煌文献记载"],
      "significance": "宗教艺术融合"
    },
    {
      "period": "唐宋",
      "stage": "繁荣期",
      "characteristics": ["题材丰富", "融入生活场景", "节日应用"],
      "evidence": ["诗词记载", "节日习俗"],
      "significance": "民俗化发展"
    },
    {
      "period": "明清",
      "stage": "鼎盛期",
      "characteristics": ["民俗化成熟", "形成地方特色", "技法体系化"],
      "evidence": ["地方志记载", "传世作品"],
      "significance": "安塞特色形成"
    },
    {
      "period": "民国",
      "stage": "传承期",
      "characteristics": ["技法完善", "纹样体系化", "师徒传承"],
      "evidence": ["老艺人回忆", "家传作品"],
      "significance": "传统延续"
    },
    {
      "period": "建国后",
      "stage": "保护期",
      "characteristics": ["非遗认定", "创新发展", "教育推广"],
      "evidence": ["非遗名录", "传承人认定"],
      "significance": "现代化保护"
    }
  ],

  "regional_schools": {
    "真武洞镇": {
      "characteristics": ["粗犷豪放", "阴阳对比强烈", "动物题材擅长"],
      "representative_artists": ["曹佃祥", "白凤莲", "王西安"],
      "representative_patterns": ["下山虎", "抓髻娃娃", "狮舞"],
      "description": "风格雄浑有力，充满黄土高原气息"
    },
    "沿河湾镇": {
      "characteristics": ["细腻流畅", "线条优美", "植物题材擅长"],
      "representative_artists": ["李秀芳", "高金爱", "张芝兰"],
      "representative_patterns": ["鱼戏莲", "凤凰牡丹", "百花图"],
      "description": "风格柔美精致，注重细节刻画"
    },
    "化子坪镇": {
      "characteristics": ["古朴厚重", "民俗气息浓郁", "故事题材擅长"],
      "representative_artists": ["胡凤莲", "薛玉琴", "赵秀兰"],
      "representative_patterns": ["老鼠嫁女", "灶神", "孟姜女"],
      "description": "风格传统厚重，民俗内涵丰富"
    }
  },

  "patterns_library": {
    "auspicious_patterns": {
      "category": "吉祥纹样",
      "count": 128,
      "subcategories": [
        {
          "name": "福禄寿喜",
          "patterns": [
            {
              "id": "FLS001",
              "name": "五福捧寿",
              "meaning": "长寿安康，五福临门",
              "composition": "五只蝙蝠环绕篆书寿字",
              "application": ["寿诞", "春节", "老人居室"],
              "technique": "阳刻为主，阴刻点缀",
              "difficulty_level": 3,
              "cultural_story": "源自《尚书·洪范》：一曰寿、二曰富、三曰康宁、四曰攸好德、五曰考终命",
              "related_patterns": ["FLS002", "FLS003"],
              "suitable_age": "10岁以上",
              "teaching_points": ["对称构图", "谐音文化", "篆书认识"],
              "image_references": ["fls001_line.png", "fls001_color.jpg", "fls001_steps.gif"]
            },
            {
              "id": "FLS002",
              "name": "禄星高照",
              "meaning": "官运亨通，前程似锦",
              "composition": "禄星持如意，梅花鹿相伴",
              "application": ["考试", "晋升", "书房"],
              "technique": "线面结合，阴阳刻并用",
              "difficulty_level": 4,
              "cultural_story": "道教信仰中的禄星，主管功名利禄",
              "related_patterns": ["FLS001", "FLS004"],
              "suitable_age": "12岁以上",
              "teaching_points": ["人物造型", "祥云表现", "吉祥物搭配"]
            }
          ]
        },
        {
          "name": "多子多福",
          "patterns": [
            {
              "id": "DZF001",
              "name": "榴开百子",
              "meaning": "子孙满堂，家族兴旺",
              "composition": "开裂石榴露出饱满籽粒",
              "application": ["婚庆", "生育", "新房"],
              "technique": "阴刻籽粒，阳刻果皮",
              "difficulty_level": 3,
              "cultural_story": "北齐安德王纳妃，妃母宋氏以石榴相赠，寓意多子",
              "related_patterns": ["DZF002", "DZF003"],
              "suitable_age": "10岁以上",
              "teaching_points": ["果实表现", "籽粒排列", "开裂质感"]
            }
          ]
        }
      ]
    },

    "zodiac_patterns": {
      "category": "生肖纹样",
      "count": 60,
      "patterns_by_zodiac": {
        "鼠": [
          {
            "variant": "老鼠偷油",
            "meaning": "聪明机智，生活智慧",
            "composition": "老鼠倒挂油瓶",
            "folklore": "元宵节故事，老鼠聪明偷油",
            "difficulty": 2,
            "application": ["儿童房", "元宵节装饰"]
          },
          {
            "variant": "老鼠嫁女",
            "meaning": "喜庆吉祥，热闹非凡",
            "composition": "仪仗队伍，抬花轿",
            "folklore": "正月二十五老鼠嫁女日",
            "difficulty": 4,
            "application": ["春节", "婚庆主题"]
          }
        ],
        "牛": [
          {
            "variant": "春牛图",
            "meaning": "春耕开始，丰收期盼",
            "composition": "牧童骑牛，柳枝飘扬",
            "folklore": "立春鞭春牛习俗",
            "difficulty": 3,
            "application": ["立春节气", "农业宣传"]
          }
        ]
      }
    },

    "folklore_stories": {
      "category": "民俗故事",
      "count": 45,
      "stories": [
        {
          "id": "MSG001",
          "title": "孟姜女哭长城",
          "source": "民间传说，四大民间故事之一",
          "scenes": [
            {
              "sequence": 1,
              "content": "范喜良被抓修长城",
              "composition": "官兵押解，夫妻离别",
              "key_elements": ["官兵", "枷锁", "哭别"]
            },
            {
              "sequence": 2,
              "content": "孟姜女千里寻夫",
              "composition": "跋山涉水，风雨兼程",
              "key_elements": ["包袱", "雨伞", "山路"]
            },
            {
              "sequence": 3,
              "content": "哭倒长城八百里",
              "composition": "城墙崩塌，白骨露出",
              "key_elements": ["倒塌城墙", "白骨", "痛哭"]
            },
            {
              "sequence": 4,
              "content": "跳海殉情",
              "composition": "海浪滔天，化作礁石",
              "key_elements": ["大海", "礁石", "衣裙"]
            }
          ],
          "cultural_significance": "忠贞爱情，反抗暴政，民间抗争精神",
          "educational_value": "历史教育，情感培养，正义感建立",
          "suitable_age": "12岁以上",
          "teaching_duration": "120分钟"
        }
      ]
    },

    "festival_patterns": {
      "category": "节日庆典",
      "count": 32,
      "festivals": {
        "春节": {
          "patterns": [
            {
              "name": "年年有余",
              "elements": ["鲤鱼", "莲花", "水波纹"],
              "placement": "窗户、米缸、灶台",
              "meaning": "生活富足，连年有余",
              "color": "红色为主，金色点缀"
            },
            {
              "name": "福到啦",
              "elements": ["倒福字", "童子", "蝙蝠"],
              "placement": "大门、厅堂",
              "meaning": "福气临门，吉祥如意",
              "color": "大红底色，黑色剪影"
            }
          ],
          "customs": "贴窗花、挂笺、门神"
        },
        "元宵节": {
          "patterns": [
            {
              "name": "灯会图",
              "elements": ["灯笼", "人物", "舞龙"],
              "placement": "灯棚、公共场所",
              "meaning": "喜庆团圆，光明希望",
              "color": "五彩缤纷"
            }
          ],
          "customs": "赏灯、猜谜、吃元宵"
        }
      }
    },

    "wedding_patterns": {
      "category": "婚嫁礼仪",
      "count": 28,
      "stages": {
        "proposal": {
          "stage_name": "提亲阶段",
          "patterns": [
            {
              "name": "龙凤帖",
              "usage": "婚书装饰",
              "meaning": "天作之合，龙凤呈祥",
              "elements": ["龙", "凤", "祥云"]
            }
          ]
        },
        "wedding_day": {
          "stage_name": "婚礼当天",
          "patterns": [
            {
              "name": "双喜字",
              "usage": "各处张贴（门窗、家具、用品）",
              "meaning": "双重喜庆，好事成双",
              "elements": ["双喜字", "心形", "花朵"],
              "variants": ["圆喜", "方喜", "花边喜"]
            },
            {
              "name": "和合二仙",
              "usage": "新房装饰",
              "meaning": "夫妻和睦，百年好合",
              "elements": ["寒山", "拾得", "宝盒", "荷花"]
            }
          ]
        }
      }
    }
  },

  "techniques_library": {
    "scissor_techniques": [
      {
        "id": "SC001",
        "name": "直剪法",
        "description": "剪直线条",
        "suitable_for": ["边框", "枝干", "直线纹样"],
        "key_points": ["剪刀不动纸移动", "手腕稳定", "视线跟随"],
        "difficulty": 1,
        "practice_materials": ["长条纸", "方格纸"]
      },
      {
        "id": "SC002",
        "name": "曲剪法",
        "description": "剪曲线条",
        "suitable_for": ["花瓣", "云纹", "波浪"],
        "key_points": ["手腕柔和转动", "小段连接", "保持流畅"],
        "difficulty": 2,
        "practice_materials": ["波浪模板", "圆形纸"]
      }
    ],

    "knife_techniques": [
      {
        "id": "KN001",
        "name": "阳刻",
        "description": "留线去面，线条为主",
        "characteristics": ["线条连续", "空白背景", "强调轮廓"],
        "suitable_for": ["人物", "文字", "边框"],
        "tools": ["刻刀", "垫板"],
        "difficulty": 3
      },
      {
        "id": "KN002",
        "name": "阴刻",
        "description": "留面去线，块面为主",
        "characteristics": ["块面连续", "线条断开", "强调整体"],
        "suitable_for": ["大面积图案", "背景", "阴影"],
        "tools": ["刻刀", "垫板"],
        "difficulty": 3
      }
    ],

    "composition_methods": {
      "symmetry": {
        "types": ["轴对称", "中心对称", "旋转对称"],
        "applications": ["团花", "窗花", "门笺"],
        "representative_patterns": ["双喜字", "团寿纹", "雪花纹"],
        "teaching_sequence": ["对折练习", "四折练习", "多折练习"]
      },
      "balance": {
        "types": ["大小均衡", "疏密均衡", "动静均衡"],
        "applications": ["故事场景", "生活画面", "风景"],
        "representative_patterns": ["老鼠嫁女", "春耕图", "集市"],
        "teaching_sequence": ["重心练习", "疏密练习", "动感练习"]
      }
    },

    "color_systems": {
      "traditional": {
        "red_series": [
          {
            "name": "正红",
            "hex": "#d32f2f",
            "meaning": "吉祥喜庆",
            "usage": ["春节", "婚庆", "庆典"]
          },
          {
            "name": "朱红",
            "hex": "#ef5350",
            "meaning": "热烈欢快",
            "usage": ["节日", "儿童作品"]
          }
        ],
        "rules": "单色为主，节日用红，白事用白，特殊情况用彩"
      },
      "modern": {
        "color_techniques": [
          {
            "name": "衬色",
            "description": "背后衬不同颜色纸",
            "effect": "色彩对比，层次丰富"
          },
          {
            "name": "套色",
            "description": "不同颜色纸叠加剪刻",
            "effect": "色彩渐变，立体感强"
          }
        ],
        "color_combinations": [
          {
            "combination": "红+金",
            "effect": "富丽堂皇",
            "usage": ["重要庆典", "礼品装饰"]
          },
          {
            "combination": "红+黑",
            "effect": "古朴厚重",
            "usage": ["传统展示", "历史题材"]
          }
        ]
      }
    }
  },

  "inheritors_database": [
    {
      "id": "CR001",
      "name": "曹佃祥",
      "gender": "女",
      "birth_year": 1921,
      "death_year": 1988,
      "hometown": "安塞真武洞镇",
      "artistic_characteristics": ["粗犷豪放", "善剪动物", "构图饱满", "刀法有力"],
      "representative_works": [
        {
          "title": "下山虎",
          "year": 1978,
          "characteristics": ["威猛生动", "阴阳对比", "动态感强"],
          "collection": "中国美术馆"
        },
        {
          "title": "抓髻娃娃",
          "year": 1982,
          "characteristics": ["造型古朴", "寓意深刻", "对称完美"],
          "collection": "陕西非遗中心"
        }
      ],
      "teaching_career": {
        "students_count": 30,
        "teaching_years": 25,
        "teaching_method": ["口传心授", "示范指导", "实践为主"]
      },
      "honors": [
        "国家级非物质文化遗产代表性传承人",
        "中国民间工艺美术大师",
        "陕西省劳动模范"
      ],
      "famous_quotes": ["剪随心动，纸传真情", "一把剪刀剪出黄土魂"],
      "legacy": "开创真武洞流派，培养大批传承人",
      "multimedia": {
        "photos": ["cr001_photo1.jpg", "cr001_photo2.jpg"],
        "videos": ["cr001_interview.mp4"],
        "works": ["cr001_work1.jpg", "cr001_work2.jpg"]
      }
    },
    {
      "id": "CR002",
      "name": "白凤莲",
      "gender": "女",
      "birth_year": 1928,
      "death_year": 2019,
      "hometown": "安塞沿河湾镇",
      "artistic_characteristics": ["细腻生动", "故事性强", "线条优美", "情感丰富"],
      "representative_works": [
        {
          "title": "老鼠嫁女",
          "year": 1995,
          "characteristics": ["场面宏大", "人物众多", "细节精致"],
          "collection": "国家博物馆"
        }
      ],
      "teaching_career": {
        "students_count": 40,
        "teaching_years": 30,
        "teaching_method": ["社区传承", "集体教学", "鼓励创新"]
      },
      "honors": [
        "中国民间文化杰出传承人",
        "全国三八红旗手",
        "陕西省工艺美术大师"
      ],
      "famous_quotes": ["一把剪刀剪出人生百态", "纸上乾坤大，剪中日月长"],
      "legacy": "推动剪纸进社区，扩大影响力",
      "multimedia": {
        "photos": ["cr002_photo1.jpg"],
        "videos": ["cr002_demo.mp4"],
        "works": ["cr002_work1.jpg"]
      }
    }
  ],

  "folklore_connections": {
    "solar_terms": [
      {
        "term": "立春",
        "custom": "鞭春牛",
        "pattern": "春牛图",
        "meaning": "春耕开始，祈求丰收",
        "activity": "剪纸春牛，鞭打仪式"
      },
      {
        "term": "清明",
        "custom": "祭祖扫墓",
        "pattern": "柳枝燕子",
        "meaning": "怀念先人，春天到来",
        "activity": "剪纸祭品，插柳习俗"
      }
    ],
    "life_rituals": {
      "birth": {
        "patterns": ["生肖符", "长命锁", "虎头鞋样"],
        "meaning": "保平安，健康成长",
        "rituals": ["满月礼", "百天礼", "周岁礼"]
      },
      "wedding": {
        "patterns_count": "50-100幅",
        "required_patterns": ["双喜字", "龙凤呈祥", "鸳鸯戏水", "和合二仙"],
        "placement": ["新房", "嫁妆", "婚车", "宴席"],
        "meaning": "祝福新人，喜庆吉祥"
      }
    },
    "folk_beliefs": {
      "nature_worship": [
        {
          "object": "太阳",
          "pattern": "三足鸟",
          "meaning": "光明温暖，生命之源",
          "ritual": "祭祀日神"
        }
      ],
      "ancestor_worship": [
        {
          "object": "家神",
          "pattern": "祖先牌位装饰",
          "function": "祭祀供奉",
          "placement": "祠堂、家堂"
        }
      ]
    }
  },

  "education_system": {
    "grade_levels": {
      "kindergarten": {
        "age_range": "3-6岁",
        "cognitive_goals": ["认识剪刀", "分辨红纸", "知道剪纸是艺术"],
        "skill_goals": ["安全使用剪刀", "剪直线曲线", "贴纸"],
        "emotional_goals": ["感受色彩美", "体验动手乐", "培养专注力"],
        "recommended_hours": 8,
        "lesson_duration": 20,
        "curriculum": [
          {
            "unit": 1,
            "title": "认识好朋友",
            "content": ["认识剪刀", "认识纸", "安全规则"],
            "materials": ["安全剪刀", "彩色纸", "胶棒"]
          }
        ]
      },
      "primary_lower": {
        "age_range": "7-9岁",
        "cognitive_goals": ["了解安塞剪纸", "认识5种基本纹样", "知道对称概念"],
        "skill_goals": ["掌握对折剪", "剪简单纹样", "完成窗花"],
        "emotional_goals": ["热爱传统文化", "建立文化自信", "培养耐心"],
        "recommended_hours": 16,
        "lesson_duration": 40
      }
    },

    "common_questions": [
      {
        "category": "technical",
        "question": "剪曲线时总是断怎么办？",
        "answer": "剪刀角度保持45°，手腕放松转动，不要剪太急，使用锋利剪刀",
        "tips": ["先练习小弧度", "分段剪", "保持纸张平整"]
      },
      {
        "category": "technical",
        "question": "阴刻时纸容易破怎么办？",
        "answer": "使用较厚的宣纸，刻刀要保持锋利，垫板要平整，力度要均匀",
        "tips": ["从边缘开始", "先刻大面积", "及时清理纸屑"]
      }
    ],

    "activity_templates": [
      {
        "id": "ACT001",
        "title": "春节窗花工作坊",
        "duration": "2小时",
        "target_age": "8-12岁",
        "group_size": "15-20人",
        "materials": ["红纸", "剪刀", "模板", "胶水", "展示板"],
        "goals": ["了解春节习俗", "掌握窗花技法", "完成春节作品", "培养团队合作"],
        "process": [
          {
            "step": 1,
            "title": "春节文化导入",
            "duration": 15,
            "content": "讲解春节习俗，展示传统窗花"
          },
          {
            "step": 2,
            "title": "技法示范",
            "duration": 20,
            "content": "示范对折剪法，讲解注意事项"
          }
        ],
        "evaluation": ["作品完成度", "技法掌握", "创意表现", "团队合作"]
      }
    ]
  },

  "pattern_recognition_features": {
    "抓髻娃娃": {
      "key_features": ["对称人形", "头梳双髻", "手抓吉祥物", "正面站立", "服饰花纹"],
      "proportion": "头身比例1:3",
      "variants": [
        {
          "name": "抓鸡娃娃",
          "difference": "手抓公鸡",
          "meaning": "大吉大利"
        },
        {
          "name": "抓钱娃娃",
          "difference": "手抓铜钱",
          "meaning": "招财进宝"
        }
      ],
      "recognition_tips": "重点观察头部双髻和手中物品"
    },
    "鱼戏莲": {
      "key_features": ["鱼在莲间穿梭", "莲花盛开", "水波纹背景", "S形构图"],
      "meaning_association": "鱼=余，莲=连，寓意连年有余",
      "seasonal": "夏季题材",
      "application": ["春节", "婚庆", "商业场所"]
    }
  },

  "digital_resources": {
    "images": {
      "pattern_line_drawings": "patterns/line/",
      "pattern_color_works": "patterns/color/",
      "step_by_step_tutorials": "tutorials/steps/",
      "artists_photos": "artists/photos/",
      "activity_records": "activities/photos/"
    },
    "videos": {
      "technique_tutorials": "videos/techniques/",
      "artist_interviews": "videos/interviews/",
      "activity_recordings": "videos/activities/",
      "cultural_documentaries": "videos/documentaries/"
    },
    "documents": {
      "teaching_plans": "docs/teaching/",
      "research_papers": "docs/research/",
      "historical_records": "docs/history/",
      "pattern_catalogs": "docs/catalogs/"
    },
    "interactive": {
      "ar_models": "interactive/ar/",
      "3d_models": "interactive/3d/",
      "quizzes": "interactive/quizzes/",
      "games": "interactive/games/"
    }
  },

  "statistics": {
    "total_patterns": 348,
    "pattern_categories": 6,
    "artists_recorded": 23,
    "techniques_documented": 20,
    "teaching_resources": 156,
    "activity_templates": 45,
    "digital_images": 1245,
    "video_hours": 78.5,
    "document_pages": 2340
  },

  "update_log": [
    {
      "date": "2024-01-20",
      "version": "2.0.0",
      "changes": [
        "新增纹样识别特征库",
        "完善教育体系内容",
        "增加多媒体资源链接",
        "优化数据结构"
      ],
      "contributors": ["安塞文化馆", "非遗保护中心", "技术团队"]
    },
    {
      "date": "2023-12-15",
      "version": "1.5.0",
      "changes": [
        "新增传承人详细资料",
        "完善技法分类",
        "增加民俗关联"
      ]
    }
  ],

  "contact": {
    "organization": "安塞剪纸非物质文化遗产保护中心",
    "address": "陕西省延安市安塞区文化路88号",
    "phone": "0911-6212345",
    "email": "ansu_papercut@culture.gov.cn",
    "website": "http://www.ansu-papercut.cn",
    "wechat": "安塞剪纸非遗中心"
  },

  "license": {
    "type": "CC BY-NC-SA 4.0",
    "description": "知识共享 署名-非商业性使用-相同方式共享 4.0 国际许可协议",
    "permissions": ["分享", "改编"],
    "restrictions": ["商业用途需授权", "必须署名", "相同方式共享"],
    "attribution": "使用本知识库请注明来源：安塞剪纸非遗文化知识库"
  }
}