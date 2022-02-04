import random

ALL_CHENG_YU = [
    ['爱不释手', ('ai', 'bu', 'shi', 'shou'), 'To love something too much to part with it'],
    ['爱屋及乌', ('ai', 'wu', 'ji', 'wu'), 'Love me, love my dog'],
    ['按部就班', ('an', 'bu', 'jiu', 'ban'), 'To follow the prescribed order'],
    ['安居乐业', ('an', 'ju', 'le', 'ye'), 'To live in peace, without disturbance'],
    ['安贫乐道', ('an', 'pin', 'le', 'dao'), 'Happy to live a virtuous life even if in a state of poverty'],
    ['白发苍苍', ('bai', 'fa', 'cang', 'cang'), 'From white hairs'],
    ['百年树人', ('bai', 'nian', 'shu', 'ren'), 'It takes a long time to develop a person.'],
    ['百折不挠', ('bai', 'zhe', 'bu', 'nao'), 'To keep on fighting in spite of all setbacks'],
    ['班门弄斧', ('ban', 'men', 'nong', 'fu'), "To display one's slight skill before an expert"],
    ['半途而废', ('ban', 'tu', 'er', 'fei'), 'To give up halfway'],
    ['包罗万象', ('bao', 'luo', 'wan', 'xiang'), 'All-embracing'],
    ['避而不见', ('bi', 'er', 'bu', 'jian'), 'To avoid meeting someone'],
    ['闭门造车', ('bi', 'men', 'zao', 'che'), 'To disregard the outside world while doing something'],
    ['变本加厉', ('bian', 'ben', 'jia', 'li'), 'To become more intense/aggravate'],
    ['标新立异', ('biao', 'xin', 'li', 'yi'), 'To display originality'],
    ['别出心裁', ('bie', 'chu', 'xin', 'cai'), 'To adopt an original approach'],
    ['彬彬有礼', ('bin', 'bin', 'you', 'li'), 'Sophisticated'],
    ['宾至如归', ('bin', 'zhi', 'ru', 'gui'), 'Make your guests feel at home'],
    ['不耻下问', ('bu', 'chi', 'xia', 'wen'), 'Not ashamed to ask'],
    ['不得其法', ('bu', 'de', 'qi', 'fa'), 'Not knowing the right way'],
    ['不攻自破', ('bu', 'gong', 'zi', 'po'), 'Collapses on its own'],
    ['不顾一切', ('bu', 'gu', 'yi', 'qie'), 'Indifferent to everything'],
    ['不可得兼', ('bu', 'ke', 'de', 'jian'), "You can't have both at the same time"],
    ['不可救药', ('bu', 'ke', 'jiu', 'yao'), 'Incurable'],
    ['不可开交', ('bu', 'ke', 'kai', 'jiao'), 'Extremely (busy)'],
    ['不可思议', ('bu', 'ke', 'si', 'yi'), 'Inconceivable; unimaginable'],
    ['不劳而获', ('bu', 'lao', 'er', 'huo'), 'To reap without sowing'],
    ['不谋而合', ('bu', 'mou', 'er', 'he'), 'To agree without discussion'],
    ['不省人事', ('bu', 'sheng', 'ren', 'shi'), 'To lose consciousness'],
    ['不务正业', ('bu', 'wu', 'zheng', 'ye'), 'Engage in dishonest work'],
    ['不翼而飞', ('bu', 'yi', 'er', 'fei'), 'To disappear without trace'],
    ['不以为然', ('bu', 'yi', 'wei', 'ran'), 'To consider something unacceptable'],
    ['不遗余力', ('bu', 'yi', 'yu', 'li'), "To do one's utmost"],
    ['不择手段', ('bu', 'ze', 'shou', 'duan'), 'By fair means or foul'],
    ['不自觉地', ('bu', 'zi', 'jue', 'di'), 'Unconsciously'],
    ['不自量力', ('bu', 'zi', 'liang', 'li'), 'To overestimate yourself'],
    ['不足挂齿', ('bu', 'zu', 'gua', 'chi'), 'Nothing to talk about'],
    ['擦肩而过', ('ca', 'jian', 'er', 'guo'), 'To brush up against someone in passing'],
    ['长年累月', ('chang', 'nian', 'lei', 'yue'), 'Year in, year out'],
    ['趁火打劫', ('chen', 'huo', 'da', 'jie'), "To take advantage of someone's bad situation"],
    ['沉鱼落雁', ('chen', 'yu', 'luo', 'yan'), 'Extremely beautiful'],
    ['乘风破浪', ('cheng', 'feng', 'po', 'lang'), 'To have great ambitions'],
    ['程门立雪', ('cheng', 'men', 'li', 'xue'), 'To honor the master and respect his teachings'],
    ['成千上万', ('cheng', 'qian', 'shang', 'wan'), 'Thousands'],
    ['称兄道弟', ('cheng', 'xiong', 'dao', 'di'), 'To be like brothers with someone; to have a great relationship'],
    ['愁眉不展', ('chou', 'mei', 'bu', 'zhan'), 'With a worried frown'],
    ['出类拔萃', ('chu', 'lei', 'ba', 'cui'), 'To excel'],
    ['川流不息', ('chuan', 'liu', 'bu', 'xi'), 'Flows unendingly'],
    ['垂垂老矣', ('chui', 'chui', 'lao', 'yi'), 'Always older'],
    ['吹毛求疵', ('chui', 'mao', 'qiu', 'ci'), 'To be fastidious'],
    ['垂涎三尺', ('chui', 'xian', 'san', 'chi'), 'To drool (over)'],
    ['唇亡齿寒', ('chun', 'wang', 'chi', 'han'), 'To be interdependent'],
    ['从容不迫', ('cong', 'rong', 'bu', 'po'), 'Calm'],
    ['从善如流', ('cong', 'shan', 'ru', 'liu'), "Accepting of other's views"],
    ['措手不及', ('cuo', 'shou', 'bu', 'ji'), 'No time to deal with it'],
    ['打草惊蛇', ('da', 'cao', 'liang', 'she'), 'To inadvertently alert an enemy'],
    ['大刀阔斧', ('da', 'dao', 'kuo', 'fu'), 'Bold and decisive'],
    ['大公无私', ('da', 'gong', 'wu', 'si'), 'Selfless'],
    ['大汗淋漓', ('da', 'han', 'lin', 'li'), 'To be soaked with sweat'],
    ['大惊小怪', ('da', 'liang', 'xiao', 'guai'), 'Great fuss over something ordinary; to complain unjustifiably'],
    ['大言不惭', ('da', 'yan', 'bu', 'can'), 'To boast shamelessly'],
    ['大智若愚', ('da', 'zhi', 'ruo', 'yu'), 'The wise one appears stupid'],
    ['当机立断', ('dang', 'ji', 'li', 'duan'), 'To be decisive'],
    ['道听途说', ('dao', 'ting', 'tu', 'shuo'), 'To spread gossip'],
    ['得寸进尺', ('de', 'cun', 'jin', 'chi'), 'To be greedy after getting a little'],
    ['德高望重', ('de', 'gao', 'wang', 'zhong'), 'A person of virtue and prestige'],
    ['得过且过', ('de', 'guo', 'qie', 'guo'), 'Satisfied just to get through'],
    ['得意忘形', ('de', 'yi', 'wang', 'xing'), 'So happy you forget yourself'],
    ['低三下四', ('di', 'san', 'xia', 'si'), 'Mean, petty'],
    ['东山再起', ('dong', 'shan', 'zai', 'qi'), 'To stage a return'],
    ['独一无二', ('du', 'yi', 'wu', 'er'), 'Unique'],
    ['对牛弹琴', ('dui', 'niu', 'dan', 'qin'), 'To preach to deaf ears'],
    ['婀娜多姿', ('e', 'nuo', 'duo', 'zi'), 'To be graceful'],
    ['耳濡目染', ('er', 'ru', 'mu', 'ran'), 'To be influenced'],
    ['耳听为虚', ('er', 'ting', 'wei', 'xu'), 'To not believe in what you hear'],
    ['发扬光大', ('fa', 'yang', 'guang', 'da'), 'To develop and promote'],
    ['废寝忘食', ('fei', 'qin', 'wang', 'shi'), 'To neglect sleep and food'],
    ['奋不顾身', ('fen', 'bu', 'gu', 'shen'), 'Undaunted by dangers'],
    ['风驰电掣', ('feng', 'chi', 'dian', 'che'), 'Fast as lightning'],
    ['奉公守法', ('feng', 'gong', 'shou', 'fa'), 'To observe the law'],
    ['凤毛麟角', ('feng', 'mao', 'lin', 'jiao'), 'An extremely rare object'],
    ['富贵荣华', ('fu', 'gui', 'rong', 'hua'), 'Riches and honour'],
    ['敷衍塞责', ('fu', 'yan', 'sai', 'ze'), 'To skimp on the job'],
    ['改过自新', ('gai', 'guo', 'zi', 'xin'), 'To turn over a new leaf'],
    ['高瞻远瞩', ('gao', 'zhan', 'yuan', 'zhu'), 'Taking the long and broad view'],
    ['高枕无忧', ('gao', 'zhen', 'wu', 'you'), 'To sleep peacefully'],
    ['隔岸观火', ('ge', 'an', 'guan', 'huo'), 'To watch a crisis and do nothing'],
    ['各有千秋', ('ge', 'you', 'qian', 'qiu'), 'Each has its own merits'],
    ['根深蒂固', ('gen', 'shen', 'di', 'gu'), 'Deep-rooted (problem etc)'],
    ['功亏一篑', ('gong', 'yu', 'yi', 'kui'), 'Give up the forest for the trees'],
    ['苟且偷安', ('gou', 'qie', 'tou', 'an'), 'Making no attempt to improve oneself'],
    ['勾心斗角', ('gou', 'xin', 'dou', 'jiao'), 'To fight and scheme'],
    ['孤陋寡闻', ('gu', 'lou', 'gua', 'wen'), 'Ignorant and narrow-minded'],
    ['沽名钓誉', ('gu', 'ming', 'diao', 'yu'), 'To angle for fame'],
    ['古色古香', ('gu', 'se', 'gu', 'xiang'), 'Interesting/appealing (old locations, etc)'],
    ['孤掌难鸣', ('gu', 'zhang', 'nan', 'ming'), "You can't do things alone"],
    ['孤注一掷', ('gu', 'zhu', 'yi', 'zhi'), 'To stake all on one throw'],
    ['拐弯抹角', ('guai', 'wan', 'mo', 'jiao'), 'Beating round the bush'],
    ['莞尔一笑', ('guan', 'er', 'yi', 'xiao'), 'To give a faint smile'],
    ['光明磊落', ('guang', 'ming', 'lei', 'luo'), 'Straightforward and upright'],
    ['光明正大', ('guang', 'ming', 'zheng', 'da'), 'Honorable'],
    ['海底捞针', ('hai', 'di', 'lao', 'zhen'), 'To find a needle in a haystack'],
    ['海市蜃楼', ('hai', 'shi', 'shen', 'lou'), 'To build castles in the air; mirage'],
    ['含辛茹苦', ('han', 'xin', 'ru', 'ku'), 'To suffer bitter hardship'],
    ['好高骛远', ('hao', 'gao', 'wu', 'yuan'), 'To be overambitious'],
    ['好逸恶劳', ('hao', 'yi', 'wu', 'lao'), 'To love ease and hate work'],
    ['和睦共处', ('he', 'mu', 'gong', 'chu'), 'Peaceful coexistence'],
    ['厚德载物', ('hou', 'de', 'zai', 'wu'), 'To be of strong moral character'],
    ['狐假虎威', ('hu', 'jia', 'hu', 'wei'), 'To intimidate people with your connections'],
    ['囫囵吞枣', ('hu', 'lun', 'tun', 'zao'), 'To swallow information without assimilating it'],
    ['胡说八道', ('hu', 'shuo', 'ba', 'dao'), 'To talk nonsense'],
    ['胡思乱想', ('hu', 'si', 'luan', 'xiang'), 'To indulge in flights of fancy'],
    ['胡作非为', ('hu', 'zuo', 'fei', 'wei'), 'To run amok'],
    ['画龙点睛', ('hua', 'long', 'dian', 'jing'), 'To add the vital finishing touch'],
    ['画蛇添足', ('hua', 'she', 'tian', 'zu'), 'To ruin something by being superfluous'],
    ['花言巧语', ('hua', 'yan', 'qiao', 'yu'), 'Elegant but insincere words'],
    ['焕然一新', ('huan', 'ran', 'yi', 'xin'), 'To take on a completely new appearance'],
    ['挥金如土', ('hui', 'jin', 'ru', 'tu'), 'To squander money'],
    ['混水摸鱼', ('hun', 'shui', 'mo', 'yu'), 'Take advantage of crisis for personal gain'],
    ['火上加油', ('huo', 'shang', 'jia', 'you'), 'To throw fuel on the fire'],
    ['鸡犬不宁', ('ji', 'quan', 'bu', 'ning'), 'Pandemonium'],
    ['集思广益', ('ji', 'si', 'guang', 'yi'), 'To pool wisdom for mutual benefit'],
    ['家常便饭', ('jia', 'chang', 'bian', 'fan'), 'Routine'],
    ['假公济私', ('jia', 'gong', 'ji', 'si'), 'Abuse public position for personal gain'],
    ['家喻户晓', ('jia', 'yu', 'hu', 'xiao'), 'Understood by everyone'],
    ['见利忘义', ('jian', 'li', 'wang', 'yi'), 'Ignore morality for greed'],
    ['见钱眼开', ('jian', 'qian', 'yan', 'kai'), 'To be desirous of money'],
    ['见异思迁', ('jian', 'yi', 'si', 'qian'), 'Loving fads and novelty'],
    ['见义勇为', ('jian', 'yi', 'yong', 'wei'), "To stand up bravely for what's right"],
    ['捷足先登', ('jie', 'zu', 'xian', 'deng'), 'Early bird catches the worm'],
    ['津津有味', ('jin', 'jin', 'you', 'wei'), 'With enjoyment (food etc.)'],
    ['筋疲力尽', ('jin', 'pi', 'li', 'jin'), 'To feel exhausted'],
    ['进退两难', ('jin', 'tui', 'liang', 'nan'), 'No room to advance or to retreat'],
    ['进退维谷', ('jin', 'tui', 'wei', 'gu'), 'No room to advance or to retreat'],
    ['惊弓之鸟', ('jing', 'gong', 'zhi', 'niao'), 'Once bitten, twice shy'],
    ['井井有条', ('jing', 'jing', 'you', 'tiao'), 'Neat and tidy'],
    ['精益求精', ('jing', 'yi', 'qiu', 'jing'), 'Constantly improving'],
    ['居安思危', ('ju', 'an', 'si', 'wei'), 'Plan for danger in times of safety'],
    ['鞠躬尽瘁', ('ju', 'gong', 'jin', 'cui'), 'Spare no effort for a task'],
    ['举目无亲', ('ju', 'mu', 'wu', 'qin'), 'To be a stranger in a strange land'],
    ['举一反三', ('ju', 'yi', 'fan', 'san'), 'To deduce many things'],
    ['举足轻重', ('ju', 'zu', 'qing', 'zhong'), 'To play a critical role'],
    ['绝无仅有', ('jue', 'wu', 'jin', 'you'), 'One of a kind; unique'],
    ['开卷有益', ('kai', 'juan', 'you', 'yi'), 'Reading always brings benefits'],
    ['开门见山', ('kai', 'men', 'jian', 'shan'), 'To get right to the point'],
    ['开源节流', ('kai', 'yuan', 'jie', 'liu'), 'Increase income and reduce spending'],
    ['慷慨解囊', ('kang', 'kai', 'jie', 'nang'), 'Generous'],
    ['刻苦耐劳', ('ke', 'ku', 'nai', 'lao'), 'To work hard and overcome adversity'],
    ['可想而知', ('ke', 'xiang', 'er', 'zhi'), 'As you can well imagine'],
    ['口若悬河', ('kou', 'ruo', 'xuan', 'he'), 'Very talkative'],
    ['口是心非', ('kou', 'shi', 'xin', 'fei'), 'To not mean what you say'],
    ['苦口婆心', ('ku', 'kou', 'po', 'xin'), 'To persuade patiently'],
    ['夸大其词', ('kua', 'da', 'qi', 'ci'), 'Exaggerate'],
    ['脍炙人口', ('kuai', 'zhi', 'ren', 'kou'), 'Appealing to the masses'],
    ['滥竽充数', ('lan', 'yu', 'chong', 'shu'), 'To make up the numbers with bad goods'],
    ['狼吞虎咽', ('lang', 'tun', 'hu', 'yan'), 'To brush away food like a wolf'],
    ['老马识途', ('lao', 'ma', 'shi', 'tu'), 'Trust the experienced worker'],
    ['雷打不动', ('lei', 'da', 'bu', 'dong'), 'To be determined, unshakable'],
    ['力不从心', ('li', 'bu', 'cong', 'xin'), 'Not as strong as one wishes'],
    ['励精图治', ('li', 'jing', 'tu', 'zhi'), "To work hard (for one's country)"],
    ['理直气壮', ('li', 'zhi', 'qi', 'zhuang'), 'In the right and self-confident'],
    ['恋恋不舍', ('lian', 'lian', 'bu', 'she'), 'To be reluctant to leave'],
    ['惊慌失措', ('liang', 'huang', 'shi', 'cuo'), 'Caught in panic'],
    ['瞭如指掌', ('liao', 'ru', 'zhi', 'zhang'), 'Know something very well'],
    ['临渴掘井', ('lin', 'ke', 'jue', 'jing'), 'Seek help at the last minute'],
    ['伶牙俐齿', ('ling', 'ya', 'li', 'chi'), 'To be clear and eloquent'],
    ['流离失所', ('liu', 'li', 'shi', 'suo'), 'Destitute and homeless'],
    ['路不拾遗', ('lu', 'bu', 'shi', 'yi'), 'An honest society (e.g. during peace)'],
    ['乱七八糟', ('luan', 'qi', 'ba', 'zao'), 'In complete disorder'],
    ['落花流水', ('luo', 'hua', 'liu', 'shui'), 'To be in a sorry state'],
    ['络绎不绝', ('luo', 'yi', 'bu', 'jue'), 'Continuously without end'],
    ['落英缤纷', ('luo', 'ying', 'bin', 'fen'), 'Flower petals that fall like snowflakes'],
    ['慢条斯理', ('man', 'tiao', 'si', 'li'), 'Unhurried'],
    ['漫无目的', ('man', 'wu', 'mu', 'de'), 'To be without a goal'],
    ['满载而归', ('man', 'zai', 'er', 'gui'), 'Return from a rewarding journey'],
    ['忙里偷闲', ('mang', 'li', 'tou', 'xian'), 'To find time for pleasure between work'],
    ['毛遂自荐', ('mao', 'sui', 'zi', 'jian'), 'To recommend yourself'],
    ['眉飞色舞', ('mei', 'fei', 'se', 'wu'), 'To be exultant, exuberant'],
    ['每况愈下', ('mei', 'kuang', 'yu', 'xia'), 'To steadily deteriorate'],
    ['孟母三迁', ('meng', 'mu', 'san', 'qian'), 'A wise mother works to find a healthy educational environment for her children'],
    ['面目全非', ('mian', 'mu', 'quan', 'fei'), 'Change beyond recognition'],
    ['明目张胆', ('ming', 'mu', 'zhang', 'dan'), 'Openly and without fear'],
    ['明哲保身', ('ming', 'zhe', 'bao', 'shen'), 'A smart man protects himself'],
    ['明知故犯', ('ming', 'zhi', 'gu', 'fan'), 'Deliberate violation'],
    ['墨守成规', ('mo', 'shou', 'cheng', 'gui'), 'Hidebound by convention'],
    ['目中无人', ('mu', 'zhong', 'wu', 'ren'), 'Arrogant'],
    ['难兄难弟', ('nan', 'xiong', 'nan', 'di'), 'Brothers of misfortune'],
    ['弄巧成拙', ('nong', 'qiao', 'cheng', 'zhuo'), 'To outsmart oneself'],
    ['迫不及待', ('po', 'bu', 'ji', 'dai'), 'Impatiently waiting'],
    ['破釜沉舟', ('po', 'fu', 'chen', 'zhou'), "To cut off one's means of retreat"],
    ['铺天盖地', ('pu', 'tian', 'gai', 'di'), 'To cover over everything'],
    ['普天同庆', ('pu', 'tian', 'tong', 'qing'), 'Everybody celebrating together'],
    ['杞人忧天', ('qi', 'ren', 'you', 'tian'), 'Groundless fears'],
    ['七嘴八舌', ('qi', 'zui', 'ba', 'she'), 'Everyone is talking all at once'],
    ['前车之鉴', ('qian', 'che', 'zhi', 'jian'), 'To learn from the mistakes of the past'],
    ['千钧一发', ('qian', 'jun', 'yi', 'fa'), 'Imminent peril'],
    ['千篇一律', ('qian', 'pian', 'yi', 'lv'), 'Stereotyped and repetitive'],
    ['千山万水', ('qian', 'shan', 'wan', 'shui'), 'A long and tiring journey'],
    ['千言万语', ('qian', 'yan', 'wan', 'yu'), 'Thousands and thousands of words'],
    ['潜移默化', ('qian', 'yi', 'mo', 'hua'), 'Imperceptible influence'],
    ['千载难逢', ('qian', 'zai', 'nan', 'feng'), 'Extremely rare'],
    ['强词夺理', ('qiang', 'ci', 'duo', 'li'), 'To twist words and force logic'],
    ['青出于蓝', ('qing', 'chu', 'yu', 'lan'), 'The student surpasses the teacher'],
    ['轻而易举', ('qing', 'er', 'yi', 'ju'), 'Easy to do'],
    ['倾家荡产', ('qing', 'jia', 'dang', 'chan'), 'To lose a family fortune'],
    ['情同手足', ('qing', 'tong', 'shou', 'zu'), 'Deep friendship'],
    ['全神贯注', ('quan', 'shen', 'guan', 'zhu'), 'Absorbed, absorbed in'],
    ['全心全意', ('quan', 'xin', 'quan', 'yi'), 'To do something with all your heart'],
    ['惹是生非', ('re', 'shi', 'sheng', 'fei'), 'To start a dispute; begin a conflict'],
    ['人浮于事', ('ren', 'fu', 'yu', 'shi'), 'Too many cooks spoil the broth'],
    ['任劳任怨', ('ren', 'lao', 'ren', 'yuan'), 'Undertake a task despite criticism'],
    ['人云亦云', ('ren', 'yun', 'yi', 'yun'), 'To say what everyone says'],
    ['日积月累', ('ri', 'ji', 'yue', 'lei'), 'To accumulate for a long time'],
    ['荣华富贵', ('rong', 'hua', 'fu', 'gui'), 'Glory, splendor, wealth and rank'],
    ['如虎添翼', ('ru', 'hu', 'tian', 'yi'), 'With double the power'],
    ['如火如荼', ('ru', 'huo', 'ru', 'tu'), 'Flourishing and magnificent'],
    ['如期而至', ('ru', 'qi', 'er', 'zhi'), 'To arrive in time'],
    ['如释重负', ('ru', 'shi', 'zhong', 'fu'), "To have a weight off one's mind"],
    ['如影随形', ('ru', 'ying', 'sui', 'xing'), 'Inseparable; followed like your own shadow'],
    ['如愿以偿', ('ru', 'yuan', 'yi', 'chang'), 'Fully satisfied desires'],
    ['塞翁失马', ('sai', 'weng', 'shi', 'ma'), 'Not all bad comes to cause harm'],
    ['三思而行', ('san', 'si', 'er', 'xing'), 'Think before you act'],
    ['僧多粥少', ('seng', 'duo', 'zhou', 'shao'), 'Demand exceeds supply'],
    ['杀鸡取卵', ('sha', 'ji', 'qu', 'luan'), 'Sacrifice the long term for short term gains'],
    ['舍己为人', ('she', 'ji', 'wei', 'ren'), 'To abandon self for others'],
    ['深情厚谊', ('shen', 'qing', 'hou', 'yi'), 'Long and intimate friendship'],
    ['省吃俭用', ('sheng', 'chi', 'jian', 'yong'), 'To live frugally'],
    ['事半功倍', ('shi', 'ban', 'gong', 'bei'), 'To be efficient'],
    ['事倍功半', ('shi', 'bei', 'gong', 'ban'), 'To be inefficient'],
    ['十全十美', ('shi', 'quan', 'shi', 'mei'), 'Perfect'],
    ['视死如归', ('shi', 'si', 'ru', 'gui'), 'To be unafraid of death'],
    ['世外桃源', ('shi', 'wai', 'tao', 'yuan'), 'Paradise if peace; utopia'],
    ['手不释卷', ('shou', 'bu', 'shi', 'juan'), 'Diligent and hardworking (always with a book)'],
    ['守口如瓶', ('shou', 'kou', 'ru', 'ping'), 'Tight-lipped'],
    ['守望相助', ('shou', 'wang', 'xiang', 'zhu'), 'To help each other'],
    ['守株待兔', ('shou', 'zhu', 'dai', 'tu'), 'To expect rewards without hard work'],
    ['熟能生巧', ('shu', 'neng', 'sheng', 'qiao'), 'With familiarity you learn the trick; practice makes perfect'],
    ['束手无策', ('shu', 'shou', 'wu', 'ce'), 'Helpless in the face of a crisis'],
    ['数一数二', ('shu', 'yi', 'shu', 'er'), 'The best; considered among the best'],
    ['水到渠成', ('shui', 'dao', 'qu', 'cheng'), 'When conditions are right, success will follow'],
    ['水落石出', ('shui', 'luo', 'shi', 'chu'), 'Truth is revealed'],
    ['顺其自然', ('shun', 'qi', 'zi', 'ran'), 'To let nature take its course'],
    ['顺手牵羊', ('shun', 'shou', 'qian', 'yang'), 'Take advantage of crisis for personal gain'],
    ['说三道四', ('shuo', 'san', 'dao', 'si'), 'To gossip'],
    ['似懂非懂', ('si', 'dong', 'fei', 'dong'), 'To not fully understand'],
    ['似懂非懂', ('si', 'dong', 'fei', 'dong'), 'To not fully understand'],
    ['似懂非懂', ('si', 'dong', 'fei', 'dong'), 'To not fully understand'],
    ['似懂非懂', ('si', 'dong', 'fei', 'dong'), 'To not fully understand'],
    ['似懂非懂', ('si', 'dong', 'fei', 'dong'), 'To not fully understand'],
    ['四海为家', ('si', 'hai', 'wei', 'jia'), 'To make every place your home; live as a hobo'],
    ['司空见惯', ('si', 'kong', 'jian', 'guan'), 'A common occurrence'],
    ['死里逃生', ('si', 'li', 'tao', 'sheng'), 'To find a way out of certain death'],
    ['思前想后', ('si', 'qian', 'xiang', 'hou'), 'To accurately ponder over something'],
    ['似是而非', ('si', 'shi', 'er', 'fei'), 'Looks right but actually wrong'],
    ['厮守终身', ('si', 'shou', 'zhong', 'shen'), "To be together for one's whole life"],
    ['厮守终生', ('si', 'shou', 'zhong', 'sheng'), 'To be together forever'],
    ['随遇而安', ('sui', 'yu', 'er', 'an'), 'At home wherever one is'],
    ['损人利己', ('sun', 'ren', 'li', 'ji'), 'To seek benefit at the expense of others'],
    ['忐忑不安', ('tan', 'te', 'bu', 'an'), 'Disquieted; preoccupied; uncomfortable'],
    ['滔滔不绝', ('tao', 'tao', 'bu', 'jue'), 'Talking non-stop'],
    ['提心吊胆', ('ti', 'xin', 'diao', 'dan'), 'To be very scared and on edge'],
    ['天涯海角', ('tian', 'ya', 'hai', 'jiao'), 'Far off worlds (expressing a very large distance'],
    ['挑拨离间', ('tiao', 'bo', 'li', 'jian'), 'To sow dissension'],
    ['铤而走险', ('ting', 'er', 'zou', 'xian'), 'To take a risk out of desperation'],
    ['同甘共苦', ('tong', 'gan', 'gong', 'ku'), "To share life's joys and sorrows"],
    ['同归于尽', ('tong', 'gui', 'yu', 'jin'), 'Mutual destruction'],
    ['同流合污', ('tong', 'liu', 'he', 'wu'), "To follow other's bad example"],
    ['同舟共济', ('tong', 'zhou', 'gong', 'ji'), 'Having common goals due to a situation'],
    ['投机取巧', ('tou', 'ji', 'qu', 'qiao'), 'To seize every opportunity'],
    ['徒劳无功', ('tu', 'lao', 'wu', 'gong'), 'To work to no avail'],
    ['推陈出新', ('tui', 'chen', 'chu', 'xin'), 'To innovate'],
    ['完璧归赵', ('wan', 'bi', 'gui', 'zhao'), 'To give something back to its owner in excellent condition'],
    ['望尘莫及', ('wang', 'chen', 'mo', 'ji'), 'No hope of catching up'],
    ['忘恩负义', ('wang', 'en', 'fu', 'yi'), 'To be ungrateful'],
    ['为非作歹', ('wei', 'fei', 'zuo', 'dai'), 'To break the law'],
    ['惟妙惟肖', ('wei', 'miao', 'wei', 'xiao'), 'To be just like the real thing'],
    ['未雨绸缪', ('wei', 'yu', 'chou', 'mou'), 'To plan for rainy days'],
    ['温故知新', ('wen', 'gu', 'zhi', 'xin'), 'To review the old and know the new'],
    ['卧虎藏龙', ('wo', 'hu', 'cang', 'long'), 'Full of people with unusual talents'],
    ['我行我素', ('wo', 'xing', 'wo', 'su'), 'To stick to your own way of doing things'],
    ['无病呻吟', ('wu', 'bing', 'shen', 'yin'), 'To moan about imaginary illness'],
    ['无动于衷', ('wu', 'dong', 'yu', 'zhong'), 'Aloof'],
    ['无可奈何', ('wu', 'ke', 'nai', 'he'), 'To have no alternatives/way out'],
    ['无理取闹', ('wu', 'li', 'qu', 'nao'), 'To create problems for no reason'],
    ['无所不谈', ('wu', 'suo', 'bu', 'tan'), 'To talk about everything under the sun'],
    ['五体投地', ('wu', 'ti', 'tou', 'di'), 'To prostrate oneself in admiration'],
    ['无微不至', ('wu', 'wei', 'bu', 'zhi'), 'Meticulous'],
    ['息事宁人', ('xi', 'shi', 'ning', 'ren'), 'To keep the peace'],
    ['下不为例', ('xia', 'bu', 'wei', 'li'), 'It will not set a precedent'],
    ['相安无事', ('xiang', 'an', 'wu', 'shi'), 'To live together in harmony'],
    ['相辅相成', ('xiang', 'fu', 'xiang', 'cheng'), 'To complement one another'],
    ['相去甚远', ('xiang', 'qu', 'shen', 'yuan'), 'To make a big difference'],
    ['相濡以沫', ('xiang', 'ru', 'yi', 'mo'), 'To help each other out despite both being in delicate condition'],
    ['相提并论', ('xiang', 'ti', 'bing', 'lun'), 'To be placed at the same level of'],
    ['笑里藏刀', ('xiao', 'li', 'cang', 'dao'), 'A dagger hidden behind a smile'],
    ['小心翼翼', ('xiao', 'xin', 'yi', 'yi'), 'Extremely cautious'],
    ['心甘情愿', ('xin', 'gan', 'qing', 'yuan'), 'To be extremely happy to do something'],
    ['心灰意懒', ('xin', 'hui', 'yi', 'lan'), 'Discouraged'],
    ['信口雌黄', ('xin', 'kou', 'ci', 'huang'), 'To speak off the cuff'],
    ['信口开河', ('xin', 'kou', 'kai', 'he'), 'To speak without thinking'],
    ['心旷神怡', ('xin', 'kuang', 'shen', 'yi'), 'Carefree and relaxed'],
    ['心如止水', ('xin', 'ru', 'zhi', 'shui'), 'A peaceful heart; a heart as calm as still water'],
    ['心神不宁', ('xin', 'shen', 'bu', 'ning'), 'To feel bad about nothing'],
    ['欣欣向荣', ('xin', 'xin', 'xiang', 'rong'), 'Flourishing and thriving'],
    ['兴高采烈', ('xing', 'gao', 'cai', 'lie'), 'Happy and excited'],
    ['星火燎原', ('xing', 'huo', 'liao', 'yuan'), 'A single spark creates a blaze'],
    ['幸灾乐祸', ('xing', 'zai', 'le', 'huo'), "To enjoy others' misfortunes"],
    ['兴致勃勃', ('xing', 'zhi', 'bo', 'bo'), 'Full of enthusiasm'],
    ['胸有成竹', ('xiong', 'you', 'cheng', 'zhu'), 'To plan in advance'],
    ['袖手旁观', ('xiu', 'shou', 'pang', 'guan'), 'To look on without helpinh'],
    ['虚怀若谷', ('xu', 'huai', 'ruo', 'gu'), 'To be extremely open-minded'],
    ['栩栩如生', ('xu', 'xu', 'ru', 'sheng'), 'Vivid and lifelike'],
    ['悬崖勒马', ('xuan', 'ya', 'le', 'ma'), 'To act in the nick of time'],
    ['雪上加霜', ('xue', 'shang', 'jia', 'shuang'), 'One disaster after another'],
    ['削足适履', ('xue', 'zu', 'shi', 'lv'), 'Impractical or inelegant solution'],
    ['寻根究底', ('xun', 'gen', 'jiu', 'di'), 'Inquire deeply into'],
    ['循循善诱', ('xun', 'xun', 'shan', 'you'), 'To guide patiently and systematically'],
    ['鸦雀无声', ('ya', 'que', 'wu', 'sheng'), 'Absolute silence'],
    ['雅俗共赏', ('ya', 'su', 'gong', 'shang'), 'Can be enjoyed by scholars and lay-people alike'],
    ['眼见为实', ('yan', 'jian', 'wei', 'shi'), 'To believe in what can be seen'],
    ['言行一致', ('yan', 'xing', 'yi', 'zhi'), "To live up to one's word"],
    ['阳光明媚', ('yang', 'guang', 'ming', 'mei'), 'The sun is particularly bright'],
    ['养尊处优', ('yang', 'zun', 'chu', 'you'), 'To live like a prince'],
    ['摇摇欲坠', ('yao', 'yao', 'yu', 'zhui'), 'Tottering'],
    ['夜深人静', ('ye', 'shen', 'ren', 'jing'), 'In the silence of deepest night'],
    ['一败涂地', ('yi', 'bai', 'tu', 'di'), 'To fail utterly'],
    ['一暴十寒', ('yi', 'bao', 'shi', 'han'), 'Sporadic effort'],
    ['一本正经', ('yi', 'ben', 'zheng', 'jing'), 'To always be serious'],
    ['亦步亦趋', ('yi', 'bu', 'yi', 'qu'), 'To blindly imitate someone'],
    ['一蹴而就', ('yi', 'cu', 'er', 'jiu'), 'To be successful on the first try'],
    ['一帆风顺', ('yi', 'fan', 'feng', 'shun'), 'Have a nice trip'],
    ['一见如故', ('yi', 'jian', 'ru', 'gu'), 'Familiarity at first sight'],
    ['一箭双雕', ('yi', 'jian', 'shuang', 'diao'), 'To kill two birds with one stone'],
    ['一举两得', ('yi', 'ju', 'liang', 'de'), 'To kill two birds with one stone'],
    ['一蹶不振', ('yi', 'jue', 'bu', 'zhen'), 'Setback leading to total collapse'],
    ['一劳永逸', ('yi', 'lao', 'yong', 'yi'), 'Get something done once and for all'],
    ['以卵击石', ('yi', 'luan', 'ji', 'shi'), 'To attempt the impossible'],
    ['一落千丈', ('yi', 'luo', 'qian', 'zhang'), 'A devastating decline'],
    ['一毛不拔', ('yi', 'mao', 'bu', 'ba'), 'Stingy'],
    ['一门心思', ('yi', 'men', 'xin', 'si'), 'To be solely concentrated on doing something'],
    ['一目瞭然', ('yi', 'mu', 'liao', 'ran'), 'To understand with a glance'],
    ['一切就绪', ('yi', 'qie', 'jiu', 'xu'), 'Everything is in order'],
    ['易如反掌', ('yi', 'ru', 'fan', 'zhang'), 'Very easy'],
    ['以身作则', ('yi', 'shen', 'zuo', 'ze'), 'To be a role model'],
    ['一视同仁', ('yi', 'shi', 'tong', 'ren'), 'To treat everyone equally'],
    ['一事无成', ('yi', 'shi', 'wu', 'cheng'), 'To have achieved nothing'],
    ['一头雾水', ('yi', 'tou', 'wu', 'shui'), 'To feel confused'],
    ['一网打尽', ('yi', 'wang', 'da', 'jin'), 'To eliminate at one stroke'],
    ['异想天开', ('yi', 'xiang', 'tian', 'kai'), 'To imagine the wildest thing'],
    ['以牙还牙', ('yi', 'ya', 'huan', 'ya'), 'To retaliate'],
    ['依依不舍', ('yi', 'yi', 'bu', 'she'), 'To be reluctant to leave something'],
    ['一意孤行', ('yi', 'yi', 'gu', 'xing'), "Obstinately clinging to one's course"],
    ['一针见血', ('yi', 'zhen', 'jian', 'xie'), 'To hit the nail on the head'],
    ['一知半解', ('yi', 'zhi', 'ban', 'jie'), 'To have a partial understanding'],
    ['饮水思源', ('yin', 'shui', 'si', 'yuan'), 'To be grateful'],
    ['应接不暇', ('ying', 'jie', 'bu', 'xia'), 'More than one can attend to'],
    ['迎刃而解', ('ying', 'ren', 'er', 'jie'), 'Easily solved'],
    ['应运而生', ('ying', 'yun', 'er', 'sheng'), 'To emerge thanks to a favorable situation'],
    ['有目共睹', ('you', 'mu', 'gong', 'du'), 'Obvious to all'],
    ['优柔寡断', ('you', 'rou', 'gua', 'duan'), 'Indecisive'],
    ['游手好闲', ('you', 'shou', 'hao', 'xian'), 'To idle about'],
    ['有条不紊', ('you', 'tiao', 'bu', 'wen'), 'Methodical, systematic'],
    ['有勇无谋', ('you', 'yong', 'wu', 'mou'), 'Bold but not very astute'],
    ['愚公移山', ('yu', 'gong', 'yi', 'shan'), 'To want to is to be able to'],
    ['与日俱增', ('yu', 'ri', 'ju', 'zeng'), 'To increase steadily'],
    ['寓意深远', ('yu', 'yi', 'shen', 'yuan'), 'Morale is very low'],
    ['与众不同', ('yu', 'zhong', 'bu', 'tong'), 'Different than the crowd'],
    ['缘木求鱼', ('yuan', 'mu', 'qiu', 'yu'), 'To use counterproductive methods to do something'],
    ['再接再厉', ('zai', 'jie', 'zai', 'li'), 'To persist'],
    ['真知灼见', ('zhen', 'zhi', 'zhuo', 'jian'), 'Penetrating insight'],
    ['蒸蒸日上', ('zheng', 'zheng', 'ri', 'shang'), 'Becoming more prosperous everyday'],
    ['趾高气扬', ('zhi', 'gao', 'qi', 'yang'), 'High and mighty; arrogant'],
    ['执迷不悟', ('zhi', 'mi', 'bu', 'wu'), 'Persist in doing things wrongly'],
    ['知难而退', ('zhi', 'nan', 'er', 'tui'), 'To run from difficulty'],
    ['纸上谈兵', ('zhi', 'shang', 'tan', 'bing'), 'Armchair strategist'],
    ['志同道合', ('zhi', 'tong', 'dao', 'he'), 'Like-minded'],
    ['知行合一', ('zhi', 'xing', 'he', 'yi'), 'The union of practice and knowledge'],
    ['置之不理', ('zhi', 'zhi', 'bu', 'li'), 'To pay no heed to'],
    ['知足常乐', ('zhi', 'zu', 'chang', 'le'), 'To be content with what you have'],
    ['重蹈覆辙', ('chong', 'dao', 'fu', 'che'), 'To make the same mistakes'],
    ['重温旧梦', ('zhong', 'wen', 'jiu', 'meng'), 'To relive an old experience; relive an old dream'],
    ['忠言逆耳', ('zhong', 'yan', 'ni', 'er'), 'Good advice is often jarring'],
    ['装聋作哑', ('zhuang', 'long', 'zuo', 'ya'), 'To play deaf-mute'],
    ['惴惴不安', ('zhui', 'zhui', 'bu', 'an'), 'On thorns'],
    ['自暴自弃', ('zi', 'bao', 'zi', 'qi'), 'To abandon oneself to despair'],
    ['自力更生', ('zi', 'li', 'geng', 'sheng'), 'To be self-reliant'],
    ['自投罗网', ('zi', 'tou', 'luo', 'wang'), 'To walk right into the trap'],
    ['自相矛盾', ('zi', 'xiang', 'mao', 'dun'), 'To contradict oneself'],
    ['龇牙咧嘴', ('zi', 'ya', 'lie', 'zui'), 'To grit your teeth in pain'],
    ['自作聪明', ('zi', 'zuo', 'cong', 'ming'), 'To be presumptuous'],
    ['左顾右盼', ('zuo', 'gu', 'you', 'pan'), 'To look to the left and right'],
    ['坐井观天', ('zuo', 'jing', 'guan', 'tian'), 'Ignorant and narrow-minded'],
    ['坐享其成', ('zuo', 'xiang', 'qi', 'cheng'), 'To reap where one has not sown'],
]

def getChengYu():
    return random.choice(ALL_CHENG_YU)
