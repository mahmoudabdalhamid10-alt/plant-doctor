"""PlantVillage class registry: English/Arabic names and agronomic advice.

Label indices match the `dpdl-benchmark/plant_village` Hugging Face mirror,
which uses case-insensitive alphabetical ordering of the standard 38
PlantVillage class names (verified empirically against the official
per-class image counts from Hughes & Salathe, 2015).
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PlantClass:
    idx: int
    key: str            # machine key
    en: str             # English display name
    ar: str             # Arabic display name
    species_en: str
    species_ar: str
    healthy: bool
    advice_ar: str      # agronomic guidance in Egyptian-friendly Arabic
    advice_en: str

A = "استشر مهندسًا زراعيًا قبل استخدام أي مبيد، والتزم بجرعات النشرة الاسترشادية."
HEALTHY_AR = "النبات سليم ولا توجد علامات مرض واضحة. حافظ على الري المنتظم والتسميد المتوازن والمراقبة الدورية."
HEALTHY_EN = "The plant looks healthy. Keep up regular watering, balanced feeding and monitoring."

CLASSES = [
 PlantClass(0,"apple_scab","Apple - Apple scab","تفاح - الجرب","Apple","تفاح",False,
  f"الجرب مرض فطري. ازلِ الأوراق والثمار المصابة واطمها أو احرقها، ورُش مبيدًا فطريًا مثل الكابتان أو المانكوزيب مع بداية الموسم، وحسّن تهوية الشجرة بالتقليم. {A}",
  "Fungal disease. Remove and destroy infected leaves/fruit, spray captan or mancozeb early season, prune for airflow."),
 PlantClass(1,"apple_black_rot","Apple - Black rot","تفاح - اللفحة السوداء","Apple","تفاح",False,
  f"اللفحة السوداء فطرية. تخلّص من الثمار المومياء والأغصان المصابة بالتقليم، ورُش مبيدًا نحاسيًا أو فطريًا جهازيًا. {A}",
  "Fungal. Prune out mummified fruit and cankers, spray a copper or systemic fungicide."),
 PlantClass(2,"apple_cedar_rust","Apple - Cedar apple rust","تفاح - صدأ الأرز","Apple","تفاح",False,
  f"صدأ الأرز يحتاج أشجار العرعر ليكمل دورته. ابعد أشجار العرعر عن البستان إن أمكن، ورُش مبيدًا فطريًا (مثل ميكلوبوتانيل) في فترة الإزهار. {A}",
  "Remove nearby juniper/cedar trees if possible; spray myclobutanil around bloom."),
 PlantClass(3,"apple_healthy","Apple - Healthy","تفاح - سليم","Apple","تفاح",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(4,"blueberry_healthy","Blueberry - Healthy","توت أزرق - سليم","Blueberry","توت أزرق",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(5,"cherry_healthy","Cherry - Healthy","كرز - سليم","Cherry","كرز",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(6,"cherry_powdery_mildew","Cherry - Powdery mildew","كرز - البياض الدقيقي","Cherry","كرز",False,
  f"البياض الدقيقي فطر شائع. رُش كبريتًا زراعيًا أو مبيدًا فطريًا جهازيًا، وحسّن التهوية، وتجنّب التسميد النيتروجيني الزائد. {A}",
  "Spray horticultural sulfur or a systemic fungicide, improve airflow, avoid excess nitrogen."),
 PlantClass(7,"corn_gray_leaf_spot","Corn - Gray leaf spot","ذرة - التبقع الرمادي","Corn (maize)","ذرة",False,
  f"التبقع الرمادي فطري وينتشر مع الرطوبة. ازرع أصنافًا مقاومة، وطبّق تدوير المحاصيل وحرث بقايا المحصول، ورُش مبيدًا فطريًا (ستروبيلورين) عند ظهور الأعراض. {A}",
  "Resistant hybrids, crop rotation, residue tillage, strobilurin fungicide at first symptoms."),
 PlantClass(8,"corn_common_rust","Corn - Common rust","ذرة - الصدأ الشائع","Corn (maize)","ذرة",False,
  f"الصدأ الشائع فطري. الزراعة المبكرة والأصناف المقاومة أفضل حماية، ويمكن الرش بمبيد فطري عند الظهور المبكر. {A}",
  "Early planting and resistant hybrids; fungicide if it appears early."),
 PlantClass(9,"corn_healthy","Corn - Healthy","ذرة - سليمة","Corn (maize)","ذرة",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(10,"corn_northern_blight","Corn - Northern leaf blight","ذرة - اللفحة الشمالية","Corn (maize)","ذرة",False,
  f"اللفحة الشمالية فطرية. استخدم أصنافًا مقاومة وتدويرًا للمحاصيل، ورُش مبيدًا فطريًا عند بداية الإصابة خصوصًا مع الطقس الرطب. {A}",
  "Resistant hybrids, rotation, fungicide at onset in humid weather."),
 PlantClass(11,"grape_black_rot","Grape - Black rot","عنب - اللفحة السوداء","Grape","عنب",False,
  f"اللفحة السوداء من أخطر أمراض العنب. اجمع العناقيد والأوراق المصابة وتخلص منها، ورُش مانكوزيب أو مبيدًا جهازيًا من مرحلة ما قبل الإزهار. {A}",
  "Remove infected clusters/leaves; spray mancozeb or systemic fungicide from pre-bloom."),
 PlantClass(12,"grape_esca","Grape - Esca (black measles)","عنب - الإسكا (الحصبة السوداء)","Grape","عنب",False,
  f"الإسكا مرض خشبي مزمن بلا علاج شافٍ. قلّم الأجزاء المصابة بعيدًا عن الأنسجة السليمة وعقّم الأدوات، وخفف إجهاد الكرمة. {A}",
  "Chronic trunk disease, no full cure; prune well below symptoms, sanitize tools."),
 PlantClass(13,"grape_healthy","Grape - Healthy","عنب - سليم","Grape","عنب",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(14,"grape_leaf_blight","Grape - Leaf blight","عنب - لفحة الأوراق","Grape","عنب",False,
  f"لفحة الأوراق فطرية. ازلِ الأوراق المصابة، وحسّن التهوية داخل الكرمة، ورُش مبيدًا فطريًا وقائيًا. {A}",
  "Remove infected leaves, open the canopy, preventive fungicide."),
 PlantClass(15,"orange_hlb","Orange - Citrus greening (HLB)","برتقال - الإخضرار (التنين الأصفر)","Orange","برتقال",False,
  "الإخضرار (HLB) مرض بكتيري خطير لا علاج له. الحل الوحيد: إزالة الأشجار المصابة فورًا لحماية البستان، ومكافحة حشرة السيلا الناقلة، وزراعة شتلات معتمدة خالية. هذا التشخيص من صورة ورقة غير مؤكد؛ يجب تأكيده بتحليل معملي.",
  "HLB is a fatal bacterial disease with no cure: remove infected trees, control the psyllid vector, plant certified clean stock. Leaf-photo suspicion must be lab-confirmed."),
 PlantClass(16,"peach_bacterial_spot","Peach - Bacterial spot","خوخ - التبقع البكتيري","Peach","خوخ",False,
  f"التبقع البكتيري يزيد مع الري العلوي والجروح. رُش مبيدًا نحاسيًا في السكون وعند سقوط الأوراق، وتجنّب البلل العلوي، وازرع أصنافًا متحملة. {A}",
  "Copper sprays in dormancy/leaf fall, avoid overhead watering, tolerant varieties."),
 PlantClass(17,"peach_healthy","Peach - Healthy","خوخ - سليم","Peach","خوخ",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(18,"pepper_bacterial_spot","Bell pepper - Bacterial spot","فلفل - التبقع البكتيري","Bell pepper","فلفل",False,
  f"تبقع بكتيري ينتقل بالبذور والرذاذ. استخدم بذورًا معتمدة، وطبّق تدويرًا بعيدًا عن الطماطم والفلفل لمدة سنتين، ورُش نحاسًا وقائيًا. {A}",
  "Certified seed, 2-year rotation away from pepper/tomato, preventive copper."),
 PlantClass(19,"pepper_healthy","Bell pepper - Healthy","فلفل - سليم","Bell pepper","فلفل",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(20,"potato_early_blight","Potato - Early blight","بطاطس - الندوة المبكرة","Potato","بطاطس",False,
  f"الندوة المبكرة فطرية. ابدأ الرش الوقائي (كلوروثالونيل أو مانكوزيب) عند ظهور البقع، وطبّق تدويرًا وأزل بقايا المحصول. {A}",
  "Preventive chlorothalonil/mancozeb at first spots; rotation and residue removal."),
 PlantClass(21,"potato_healthy","Potato - Healthy","بطاطس - سليمة","Potato","بطاطس",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(22,"potato_late_blight","Potato - Late blight","بطاطس - الندوة المتأخرة","Potato","بطاطس",False,
  f"الندوة المتأخرة سريعة الانتشار وخطيرة جدًا مع الطقس الرطب. رُش مبيدًا جهازيًا (ميتالاكسيل أو سايموكسانيل) فورًا، وتخلص من النباتات شديدة الإصابة، ولا تخزن درنات من حقول مصابة. {A}",
  "Aggressive disease: immediate systemic fungicide (metalaxyl/cymoxanil), destroy heavily infected plants, never store tubers from infected fields."),
 PlantClass(23,"raspberry_healthy","Raspberry - Healthy","توت العليق - سليم","Raspberry","توت العليق",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(24,"soybean_healthy","Soybean - Healthy","فول الصويا - سليم","Soybean","فول الصويا",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(25,"squash_powdery_mildew","Squash - Powdery mildew","قرع - البياض الدقيقي","Squash","قرع (كوسة)",False,
  f"البياض الدقيقي شائع في القرعيات. رُش كبريتًا أو مبيدًا جهازيًا مبكرًا، وحسّن التهوية والمسافات، واروِ من الأسفل. {A}",
  "Early sulfur or systemic fungicide, spacing/airflow, water at the base."),
 PlantClass(26,"strawberry_healthy","Strawberry - Healthy","فراولة - سليمة","Strawberry","فراولة",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(27,"strawberry_leaf_scorch","Strawberry - Leaf scorch","فراولة - لفحة الأوراق","Strawberry","فراولة",False,
  f"لفحة الأوراق فطرية. ازلِ الأوراق المصابة القديمة، واروِ بالتنقيط بدل الرش، وجدد الزراعات القديمة، ورُش مبيدًا فطريًا عند الحاجة. {A}",
  "Remove old infected leaves, drip irrigation, renovate old beds, fungicide if needed."),
 PlantClass(28,"tomato_bacterial_spot","Tomato - Bacterial spot","طماطم - التبقع البكتيري","Tomato","طماطم",False,
  f"تبقع بكتيري ينتشر بالرذاذ والأيدي المبللة. رُش نحاسًا وقائيًا، وتجنّب العمل في الزرع المبلل، واستخدم شتلات معتمدة. {A}",
  "Preventive copper, avoid handling wet plants, certified transplants."),
 PlantClass(29,"tomato_early_blight","Tomato - Early blight","طماطم - الندوة المبكرة","Tomato","طماطم",False,
  f"الندوة المبكرة فطرية تبدأ من الأوراق السفلية. ازلِ الأوراق المصابة، وغطِّ التربة بالمهاد، ورُش كلوروثالونيل أو مانكوزيب. {A}",
  "Remove lower infected leaves, mulch, chlorothalonil/mancozeb sprays."),
 PlantClass(30,"tomato_healthy","Tomato - Healthy","طماطم - سليمة","Tomato","طماطم",True,HEALTHY_AR,HEALTHY_EN),
 PlantClass(31,"tomato_late_blight","Tomato - Late blight","طماطم - الندوة المتأخرة","Tomato","طماطم",False,
  f"الندوة المتأخرة تدمّر الزراعة في أيام مع الرطوبة. رُش مبيدًا جهازيًا فورًا (ميتالاكسيل)، وتخلص من البؤر المصابة، وراقب التقلبات الجوية. {A}",
  "Destroys crops fast in humid weather: immediate systemic fungicide, remove infection foci."),
 PlantClass(32,"tomato_leaf_mold","Tomato - Leaf mold","طماطم - عفن الأوراق","Tomato","طماطم",False,
  f"عفن الأوراق يحب رطوبة الصوب. خفّض الرطوبة بالتهوية والري الصباحي، ورُش مبيدًا فطريًا مناسبًا، وازرع أصنافًا مقاومة. {A}",
  "Reduce greenhouse humidity (ventilation, morning watering), suitable fungicide, resistant varieties."),
 PlantClass(33,"tomato_septoria","Tomato - Septoria leaf spot","طماطم - تبقع السبتوريا","Tomato","طماطم",False,
  f"تبقع السبتوريا فطري. ازلِ الأوراق السفلية المصابة، وطبّق تدويرًا 2-3 سنوات، ورُش مبيدًا فطريًا وقائيًا. {A}",
  "Remove infected lower leaves, 2-3 year rotation, preventive fungicide."),
 PlantClass(34,"tomato_spider_mites","Tomato - Spider mites","طماطم - العنكبوت الأحمر","Tomato","طماطم",False,
  f"العنكبوت الأحمر آفة حشرية دقيقة وليس فطرًا. رُش أكاروس مناسب أو زيت النيم، ورش ماء قوي تحت الأوراق، وحافظ على الأعداء الطبيعيين. {A}",
  "A mite pest, not a fungus: suitable acaricide or neem oil, strong water spray under leaves, protect beneficial insects."),
 PlantClass(35,"tomato_target_spot","Tomato - Target spot","طماطم - التبقع الهدفي","Tomato","طماطم",False,
  f"التبقع الهدفي فطري وينتشر مع الرطوبة. حسّن التهوية، واروِ من الأسفل، ورُش مبيدًا فطريًا (كلوروثالونيل أو أزوكسيستروبين). {A}",
  "Improve airflow, base watering, chlorothalonil or azoxystrobin."),
 PlantClass(36,"tomato_mosaic_virus","Tomato - Mosaic virus","طماطم - فيروس الموزاييك","Tomato","طماطم",False,
  "فيروس الموزاييك لا يُعالج بالمبيدات. اقلع النباتات المصابة وتخلص منها، واغسل الأيدي وعقّم الأدوات، وكافح المن الناقل، وازرع أصنافًا مقاومة.",
  "Virus - no spray cures it. Rogue infected plants, sanitize hands/tools, control aphids, resistant varieties."),
 PlantClass(37,"tomato_yellow_leaf_curl","Tomato - Yellow leaf curl virus","طماطم - فيروس تجعد الأوراق الصفراء","Tomato","طماطم",False,
  "فيروس تجعد الأوراق (TYLCV) ينقله الذباب الأبيض ولا علاج له. المكافحة تعتمد على الذبابة البيضاء: شِد شبكًا ناعمًا على الصوب، واستخدم أصنافًا متحملة، واقلع المصاب مبكرًا.",
  "TYLCV is whitefly-transmitted with no cure: insect netting, tolerant varieties, early roguing, whitefly control."),
]

assert len(CLASSES) == 38
BY_IDX = {c.idx: c for c in CLASSES}
BY_KEY = {c.key: c for c in CLASSES}

# PlantDoc (field-image dataset) category name -> PlantVillage class index.
PLANTDOC_TO_PV = {
    "Apple Scab Leaf": 0, "Apple leaf": 3, "Apple rust leaf": 2,
    "Bell_pepper leaf": 19, "Bell_pepper leaf spot": 18,
    "Blueberry leaf": 4, "Cherry leaf": 5,
    "Corn Gray leaf spot": 7, "Corn leaf blight": 10, "Corn rust leaf": 8,
    "Peach leaf": 17, "Potato leaf": 21,
    "Potato leaf early blight": 20, "Potato leaf late blight": 22,
    "Raspberry leaf": 23, "Soyabean leaf": 24,
    "Squash Powdery mildew leaf": 25, "Strawberry leaf": 26,
    "Tomato Early blight leaf": 29, "Tomato Septoria leaf spot": 33,
    "Tomato leaf": 30, "Tomato leaf bacterial spot": 28,
    "Tomato leaf late blight": 31, "Tomato leaf mosaic virus": 36,
    "Tomato leaf yellow virus": 37, "Tomato mold leaf": 32,
    "Tomato two spotted spider mites leaf": 34,
    "grape leaf": 13, "grape leaf black rot": 11,
}
