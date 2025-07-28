from datetime import datetime
import json

def content_dict(all_content:list[dict]):
  dic = {}
  for obj in all_content:
    heading,content = obj['heading'],obj['content']
    dic[heading] = content
  return dic

def get_content_from_selected_headings(headings:list[str],pdf_names,heading_content_mapper,input_1b,selected_headings,selected_page_numbers,selected_pdf_names)->dict:
    answer = {}

    answer['metadata'] = {
        'input_documents':pdf_names,
        'persona':input_1b['persona']['role'],
        'job_to_be_done':input_1b['job_to_be_done']['task'],
        'processing_timestamp': datetime.now().isoformat()
    }
    
    answer['extracted_sections'] = [
        {
            "document": pdf_name,
            "section_title": title,
            "importance_rank": i + 1,
            "page_number": page_no
        }
        for i, (pdf_name, title, page_no) in enumerate(zip(selected_pdf_names, selected_headings, selected_page_numbers))
    ]
    
    answer['subsection_analysis'] = [
        {"heading":heading, "refined_text":heading_content_mapper[heading],'page_number':page_no} for heading,page_no in zip(headings,selected_page_numbers)
    ]

    return answer

def get_all_content(output_1a:dict):
    all_content = []
    for k,v in output_1a.items():
       headers_contents = [ele | {'filename':k} for ele in v]
       all_content.extend(headers_contents)
    return all_content

# 1a output (personal use)
output_1a = {
    "South of France - Things to Do.pdf": [
        {
            "heading": "Introduction",
            "content": "The South of France, with its stunning coastline, picturesque villages, and vibrant cities, offers a wealth of activities and experiences for travelers. Whether you're seeking adventure, relaxation, or cultural enrichment, this region has something for everyone. This guide will take you through a variety of activities and must-see attractions to help you plan an unforgettable trip.",
            "page_number": 1
        },
        {
            "heading": "Coastal Adventures",
            "content": "The South of France is renowned for its beautiful coastline along the Mediterranean Sea. Here are some activities to enjoy by the sea:\nBeach Hopping\n• Nice: Visit the sandy shores and enjoy the vibrant Promenade des Anglais.\n• Antibes: Relax on the pebbled beaches and explore the charming old town.\n• Saint-Tropez: Experience the exclusive beach clubs and glamorous atmosphere.\n• Marseille to Cassis: Explore the stunning limestone cliffs and hidden coves of Calanques National Park.\n• Îles d'Hyères: Discover pristine beaches and excellent snorkeling opportunities on islands like Porquerolles and Port-Cros.\n• Cannes: Enjoy the sandy beaches and luxury beach clubs along the Boulevard de la Croisette.\n• Menton: Visit the serene beaches and beautiful gardens in this charming town near the Italian border.\nWater Sports\n• Cannes, Nice, and Saint-Tropez: Try jet skiing or parasailing for a thrill.\n• Toulon: Dive into the underwater world with scuba diving excursions to explore wrecks.\n• Cerbère-Banyuls: Visit the marine reserve for an unforgettable diving experience.\n• Mediterranean Coast: Charter a yacht or join a sailing tour to explore the coastline and nearby islands.\n• Marseille: Go windsurfing or kitesurfing in the windy bays.\n• Port Grimaud: Rent a paddleboard and explore the canals of this picturesque village.\n• La Ciotat: Try snorkeling in the clear waters around the Île Verte.",
            "page_number": 2
        },
        {
            "heading": "Cultural Experiences",
            "content": "The South of France is rich in history and culture. Here are some activities to immerse yourself in the region's heritage:\nArt and Museums\n• Nice: Visit the Musée Matisse, dedicated to the works of Henri Matisse.\n• Antibes: Explore the Musée Picasso, housed in the Château Grimaldi.\n• Saint-Paul-de-Vence: Discover modern art at the Fondation Maeght.\n• Aix-en-Provence: Visit the Atelier Cézanne, the studio of the famous painter Paul Cézanne.\n• Arles: Explore the Fondation Vincent van Gogh, showcasing works inspired by the artist.\n• Marseille: Visit the MuCEM (Museum of European and Mediterranean Civilizations) for a deep dive into the region's history.\n• Toulouse: Discover the Musée des Augustins, a fine arts museum housed in a former convent.\nHistorical Sites\n• Nîmes: Walk across the ancient Roman aqueduct, Pont du Gard.\n• Avignon: Explore the largest Gothic palace in Europe, Palais des Papes.\n• Carcassonne: Wander through the medieval citadel with its double walls and 52 towers.\n• Arles: Visit the Roman amphitheater and ancient theater.\n• Orange: Explore the well-preserved Roman theater and triumphal arch.\n• Aigues-Mortes: Discover the medieval walled town and its salt marshes.\n• Grasse: Visit the perfume factories and learn about the history of fragrance production.",
            "page_number": 4
        },
        {
            "heading": "Outdoor Activities",
            "content": "The diverse landscapes of the South of France offer plenty of opportunities for outdoor adventures:\nHiking and Biking\n• Verdon Gorge: Known as the \"Grand Canyon of Europe,\" offering spectacular hiking trails.\n• Luberon Regional Park: Explore picturesque villages and rolling hills, famous for lavender fields and vineyards.\n• Pyrenees National Park: Enjoy challenging hikes and stunning mountain scenery.\n• Mercantour National Park: Discover diverse wildlife and beautiful alpine landscapes.\n• Camargue: Explore the unique wetlands on horseback or by bike.\n• Mont Ventoux: Challenge yourself with a hike or bike ride up this iconic mountain.\n• Gorges du Tarn: Hike through dramatic gorges and enjoy breathtaking views.\nWater Activities\n• Ardèche River: Paddle through the stunning Ardèche Gorge.\n• Dordogne River: Enjoy a leisurely canoe trip, passing by medieval castles and charming villages.\n• Ubaye River: Experience white-water rafting for an adrenaline rush.\n• Gorges du Verdon: Rent a kayak or paddleboat to explore the turquoise waters.\n• Lake Sainte-Croix: Enjoy swimming, sailing, and windsurfing on this beautiful lake.\n• Lake Serre-Ponçon: Try water skiing or wakeboarding on one of the largest artificial lakes in Europe.\n• Cévennes National Park: Go canyoning in the rugged terrain of this beautiful park.",
            "page_number": 6
        },
        {
            "heading": "Culinary Delights",
            "content": "The South of France is a food lover's paradise. Here are some activities to indulge in the region's culinary delights:\nWine Tasting\n• Provence: Explore vineyards known for their rosé wines.\n• Languedoc: Discover diverse wines, including reds, whites, and sparkling wines.\n• Châteauneuf-du-Pape: Visit this famous wine region near Avignon.\n• Bandol: Taste the robust red wines and refreshing rosés of this coastal region.\n• Côtes du Rhône: Explore the vineyards along the Rhône River.\n• Gaillac: Discover the unique wines of this lesser-known region.\n• Bordeaux: Take a day trip to the world-renowned wine region and visit its prestigious châteaux.\nCooking Classes\n• Provence: Learn to prepare traditional dishes like ratatouille and bouillabaisse.\n• Périgord: Join a truffle hunting tour followed by a cooking class.\n• Nice: Take a class to master Niçoise cuisine, including dishes like salade niçoise and socca.\n• Toulouse: Learn to cook regional specialties such as cassoulet.\n• Marseille: Participate in a seafood cooking class to make dishes like bouillabaisse.\n• Lyon: Discover the secrets of Lyonnaise cuisine with a hands-on cooking class.\n• Sarlat: Join a foie gras workshop and learn to prepare this delicacy.",
            "page_number": 8
        },
        {
            "heading": "Festivals and Events",
            "content": "The South of France hosts a variety of festivals and events throughout the year. Here are some not-to-miss celebrations:\n• Cannes: Attend the prestigious Cannes Film Festival in May.\n• Nice: Experience the vibrant Nice Carnival in February.\n• Avignon: Enjoy the Avignon Festival in July, featuring theater, dance, and music performances.\n• Arles: Celebrate the Feria d'Arles, a traditional bullfighting festival held in April and September.\n• Menton: Visit the Lemon Festival in February, featuring elaborate citrus-themed floats and sculptures.\n• Grasse: Attend the Rose Festival in May, celebrating the town's famous flower.\n• Marseille: Experience the Fête de la Musique in June, with free concerts and performances throughout the city.",
            "page_number": 10
        },
        {
            "heading": "Relaxation and Wellness",
            "content": "For those seeking relaxation and rejuvenation, the South of France offers plenty of options:\nSpa and Wellness Retreats\n• Aix-en-Provence: Visit Thermes Sextius for thermal baths and massages.\n• Bordeaux: Enjoy vinotherapy treatments at Les Sources de Caudalie.\n• Vichy: Experience hydrotherapy and mud baths at Spa Vichy Célestins.\n• Evian-les-Bains: Relax at the Evian Resort, known for its mineral-rich waters.\n• Saint-Raphaël: Visit the Thalasso Spa for seawater treatments and relaxation.\n• Biarritz: Enjoy the luxurious spas and wellness centers in this coastal town.\n• Cannes: Indulge in a pampering session at one of the many high-end spas.\nYoga and Meditation Retreats\n• Provence: Join a yoga retreat in the serene countryside.\n• Pyrenees: Escape to the mountains for a meditation retreat.\n• Côte d'Azur: Combine relaxation with luxury at a wellness retreat.\n• Luberon: Participate in a holistic retreat with yoga, meditation, and organic meals.\n• Camargue: Enjoy a retreat focused on mindfulness and nature immersion.\n• Saint-Tropez: Find tranquility at a yoga retreat overlooking the Mediterranean.\n• Corsica: Experience a yoga and wellness retreat on this beautiful island.",
            "page_number": 11
        },
        {
            "heading": "Shopping and Markets",
            "content": "The South of France is a shopper's paradise, with a variety of markets, boutiques, and artisan shops:\nLocal Markets\n• Nice: Explore the vibrant Cours Saleya Market.\n• Cannes: Visit Marché Forville for fresh seafood and local produce.\n• Avignon: Discover local products at Marché des Halles.\n• Aix-en-Provence: Browse the stalls at the daily market on Place Richelme.\n• Saint-Rémy-de-Provence: Enjoy the lively Wednesday market with local specialties.\n• Uzès: Visit the Saturday market for fresh produce and artisanal goods.\n• Sarlat: Explore the bustling market in the heart of the medieval town.\nBoutique Shopping\n• Cannes: Shop along the famous Rue d'Antibes, lined with high-end boutiques, designer stores, and luxury brands.\n• Aix-en-Provence: Browse shops and cafes on Cours Mirabeau, an elegant boulevard with a variety of stores.\n• Nice: Find charming boutiques in the old town, offering handmade soaps, ceramics, and local crafts.\n• Saint-Tropez: Explore the chic boutiques and designer stores in this glamorous town.\n• Marseille: Visit the trendy shops in the Le Panier district, known for its artisan goods and unique finds.\n• Montpellier: Discover the boutiques in the historic Écusson district, offering fashion, jewelry, and art.\n• Toulouse: Shop in the vibrant Capitole area, home to a mix of high-end and independent stores.",
            "page_number": 13
        },
        {
            "heading": "Family-Friendly Activities",
            "content": "The South of France offers a variety of activities that are perfect for families with children:\nTheme Parks and Attractions\n• Antibes: Visit Marineland for marine shows and an aquarium.\n• Fréjus: Cool off at Aqualand water park.\n• Villeneuve-Loubet: Enjoy quirky attractions at Le Village des Fous.\n• Monteux: Spend a day at Parc Spirou, a theme park based on the famous comic book character.\n• La Palmyre: Explore the La Palmyre Zoo, home to a wide variety of animals.\n• Cap d'Agde: Have fun at Luna Park, an amusement park with rides and games.\n• Toulouse: Visit the Cité de l'Espace, a space-themed science museum with interactive exhibits.\nOutdoor Adventures\n• Verdon Gorge: Take a family hike or rent paddle boats to explore the stunning Verdon Gorge.\n• Camargue Natural Park: Explore wetlands with wild horses and flamingos, and enjoy horseback riding, bird watching, and boat tours.\n• Various Locations: Try tree-top adventure parks with zip lines, rope bridges, and climbing challenges.\n• Gorges du Tarn: Go on a family-friendly hike and enjoy the scenic views.\n• Lake Annecy: Rent bikes and ride along the lake's picturesque bike paths.\n• Pyrenees: Take a cable car ride for stunning mountain views and easy hiking trails.\n• Dordogne: Explore the region's caves and prehistoric sites with guided tours suitable for children.\nEducational Experiences\n• Toulouse: Visit Cité de l'Espace for a space-themed science museum with interactive exhibits, a planetarium, and a replica of the Mir space station.\n• Monaco: Explore the Musée Océanographique and its marine exhibits, including a shark lagoon and touch tanks.\n• Dordogne: See ancient cave paintings at prehistoric sites like Lascaux and Rouffignac, and visit museums dedicated to prehistoric life.\n• Montpellier: Discover the Planet Ocean World, an aquarium and planetarium with interactive exhibits.\n• Carcassonne: Take a guided tour of the medieval citadel and learn about its history and architecture.\n• Nîmes: Visit the Roman amphitheater and learn about ancient Roman history.\n• Arles: Explore the Roman ruins and the Musée de l'Arles Antique, which showcases artifacts from the city's past.",
            "page_number": 15
        },
        {
            "heading": "Nightlife and Entertainment",
            "content": "The South of France offers a vibrant nightlife scene, with options ranging from chic bars to lively nightclubs:\nBars and Lounges\n• Monaco: Enjoy classic cocktails and live jazz at Le Bar Americain, located in the Hôtel de Paris.\n• Nice: Try creative cocktails at Le Comptoir du Marché, a trendy bar in the old town.\n• Cannes: Experience dining and entertainment at La Folie Douce, with live music, DJs, and performances.\n• Marseille: Visit Le Trolleybus, a popular bar with multiple rooms and music styles.\n• Saint-Tropez: Relax at Bar du Port, known for its chic atmosphere and waterfront views.\n• Montpellier: Enjoy craft cocktails at Papa Doble, a speakeasy-style bar.\n• Toulouse: Sip on cocktails at Fat Cat, a stylish bar with a vintage vibe.\nNightclubs\n• Saint-Tropez: Dance at the famous Les Caves du Roy, known for its glamorous atmosphere and celebrity clientele.\n• Nice: Party at High Club on the Promenade des Anglais, featuring multiple dance floors and top DJs.\n• Cannes: Enjoy the stylish setting and rooftop terrace at La Suite, offering stunning views of Cannes.\n• Marseille: Visit R2 Rooftop, a popular nightclub with panoramic views of the city and the sea.\n• Monaco: Experience the exclusive Jimmy'z, a legendary nightclub with a luxurious ambiance.\n• Montpellier: Dance the night away at L'Antirouille, a club known for its eclectic music and lively atmosphere.\n• Toulouse: Check out Le Purple, a trendy nightclub with a vibrant dance floor and top-notch DJs.",
            "page_number": 17
        },
        {
            "heading": "Conclusion",
            "content": "The South of France is a diverse and enchanting region that offers a wide range of activities and experiences for travelers. Whether you're exploring the stunning coastline, immersing yourself in the rich cultural heritage, or indulging in the culinary delights, there is something for everyone to enjoy. From family-friendly adventures to vibrant nightlife, the South of France promises an unforgettable journey filled with memories that will last a lifetime. Use this guide to plan your trip and make the most of everything this beautiful region has to offer.",
            "page_number": 18
        }
    ],
    "South of France - Cuisine.pdf": [
        {
            "heading": "Regional Specialties",
            "content": "The South of France boasts a rich culinary heritage with distinct regional specialties that reflect the Mediterranean climate and local traditions:\nProvençal Cuisine\n• Bouillabaisse: The famous fish stew from Marseille, made with various Mediterranean fish, saffron, and rouille sauce.\n• Ratatouille: A vegetable stew featuring eggplant, zucchini, tomatoes, bell peppers, and herbs de Provence.\n• Salade Niçoise: A classic salad from Nice with tuna, hard-boiled eggs, olives, anchovies, and fresh vegetables.\n• Pissaladière: A flatbread topped with caramelized onions, olives, and anchovies, similar to pizza.\n• Socca: A chickpea pancake popular in Nice, cooked in wood-fired ovens and served hot.\nLanguedoc Specialties\n• Cassoulet: A hearty bean stew with duck, sausage, and sometimes lamb, originating from Toulouse.\n• Brandade de Morue: Salt cod puree mixed with olive oil, garlic, and sometimes potatoes.\n• Tielle Sétoise: A savory pie filled with octopus, tomatoes, and spices, from the coastal town of Sète.\n• Pélardon: A small goat cheese from the Cévennes region, often served with honey.",
            "page_number": 1
        },
        {
            "heading": "Local Ingredients",
            "content": "The South of France's cuisine is built on exceptional local ingredients that thrive in the Mediterranean climate:\nHerbs and Aromatics\n• Herbs de Provence: A blend of dried thyme, rosemary, oregano, and lavender that flavors many dishes.\n• Lavender: Used in both sweet and savory preparations, particularly in Provence.\n• Thyme: Wild thyme grows abundantly and is essential in local cooking.\n• Garlic: A cornerstone of Southern French cuisine, used generously in most dishes.\nOlives and Olive Oil\n• Tapenade: A paste made from olives, capers, and anchovies, perfect for spreading on bread.\n• Olive Varieties: Lucques, Picholine, and Nyons olives each offer unique flavors.\n• Extra Virgin Olive Oil: Cold-pressed oils from local groves enhance every meal.\nSeafood and Fish\n• Mediterranean Fish: Red mullet, sea bass, John Dory, and monkfish feature prominently.\n• Shellfish: Mussels from Bouzigues, oysters from Thau lagoon, and sea urchins.\n• Anchovies: Particularly from Collioure, used fresh or preserved in salt.",
            "page_number": 3
        },
        {
            "heading": "Wine Regions",
            "content": "The South of France produces some of the world's most diverse and exciting wines, from robust reds to elegant rosés:\nProvence Wine Region\n• Côtes de Provence: Famous for its pale pink rosé wines, perfect for summer dining.\n• Bandol: Produces powerful red wines from Mourvèdre grapes and elegant rosés.\n• Cassis: Known for crisp white wines that pair beautifully with seafood.\n• Palette: A small appellation near Aix-en-Provence producing unique terroir-driven wines.\nLanguedoc Wine Region\n• Châteauneuf-du-Pape: Prestigious red wines from 13 authorized grape varieties.\n• Côtes du Rhône: Approachable red and white wines from the Rhône Valley.\n• Corbières: Full-bodied red wines from one of France's largest appellations.\n• Minervois: Elegant wines from vineyards nestled in the foothills of the Massif Central.\n• Pic Saint-Loup: Rising star region producing exceptional red wines.\nRhône Valley\n• Hermitage: Legendary red wines from Syrah grapes and rare white wines from Marsanne and Roussanne.\n• Côte-Rôtie: Steep vineyard slopes producing some of France's most prestigious Syrah wines.\n• Condrieu: Exclusively white wines from Viognier grapes with intense floral aromas.",
            "page_number": 5
        },
        {
            "heading": "Markets and Food Shopping",
            "content": "Exploring local markets is essential for experiencing authentic Southern French food culture:\nFamous Food Markets\n• Marché aux Fleurs (Nice): Morning flower and produce market on Cours Saleya.\n• Marché des Halles (Avignon): Covered market with local specialties and fresh produce.\n• Marché Saint-Antoine (Lyon): One of France's most important food markets.\n• Marché Victor Hugo (Toulouse): Historic covered market in the city center.\n• Les Halles de Narbonne: Art Nouveau covered market with regional products.\nSpecialty Food Shops\n• Fromageries: Cheese shops featuring local goat cheeses, Roquefort, and regional varieties.\n• Charcuteries: Delicatessens with local sausages, pâtés, and cured meats.\n• Boulangeries: Bakeries offering regional breads like fougasse and pain de campagne.\n• Confiseries: Sweet shops with calissons d'Aix, nougat de Montélimar, and other regional confections.\nSeasonal Specialties\n• Summer: Tomatoes, zucchini, eggplant, melons, and stone fruits.\n• Fall: Chestnuts, mushrooms, grapes, and olive harvest.\n• Winter: Truffles, citrus fruits, and preserved foods.\n• Spring: Asparagus, artichokes, and fresh herbs.",
            "page_number": 7
        },
        {
            "heading": "Cooking Techniques",
            "content": "Southern French cooking emphasizes simple techniques that highlight the quality of local ingredients:\nTraditional Methods\n• Slow Braising: Used for dishes like daube, where meat is slowly cooked with wine and vegetables.\n• Grilling: Fish and vegetables are often grilled over aromatic wood for added flavor.\n• Confit: Duck and goose are preserved in their own fat, a technique from Southwest France.\n• En Papillote: Fish and vegetables cooked in parchment paper packets to retain moisture and flavor.\nSauce Making\n• Aioli: Garlic mayonnaise that accompanies many dishes, especially fish and vegetables.\n• Rouille: Spicy saffron sauce traditionally served with bouillabaisse.\n• Pistou: A basil, garlic, and olive oil sauce similar to Italian pesto.\n• Tapenade: Olive-based spreads that enhance bread and vegetables.\nPreservation Techniques\n• Salt Curing: Fish, particularly anchovies and cod, are preserved in salt.\n• Oil Preservation: Vegetables and cheeses stored in olive oil.\n• Drying: Tomatoes, herbs, and sausages are dried in the warm climate.\n• Pickling: Vegetables pickled in vinegar and herbs for long-term storage.",
            "page_number": 9
        }
    ],
    "South of France - History.pdf": [
        {
            "heading": "Ancient Origins",
            "content": "The South of France has been inhabited for millennia, with evidence of human presence dating back to prehistoric times:\nPrehistoric Period\n• Lascaux Cave Paintings: Dating back 17,000 years, these Paleolithic cave paintings in the Dordogne region showcase early human artistic expression.\n• Dolmens and Menhirs: Neolithic stone structures scattered across the region, particularly in Languedoc.\n• Bronze Age Settlements: Archaeological sites reveal sophisticated Bronze Age communities along the Mediterranean coast.\nGreek Colonization (600 BCE)\n• Massalia (Marseille): Founded by Greek traders from Phocaea around 600 BCE, becoming a major Mediterranean trading hub.\n• Greek Influence: Introduction of viticulture, olive cultivation, and Mediterranean agricultural techniques.\n• Trading Networks: Establishment of commercial routes connecting the Mediterranean with inland Gaul.\nCeltic Tribes\n• Ligurians: Indigenous people who inhabited the coastal regions before Greek and Roman arrival.\n• Celtic Gauls: Various tribes including the Volcae and Arverni controlled much of inland southern France.\n• Oppida: Fortified hilltop settlements that served as political and economic centers.",
            "page_number": 1
        },
        {
            "heading": "Roman Era",
            "content": "Roman conquest and rule transformed the South of France into a prosperous province known as Gallia Narbonensis:\nRoman Conquest (125-121 BCE)\n• Military Campaigns: Roman legions gradually conquered Celtic tribes and established control.\n• Provincia Romana: The region became Rome's first province beyond the Alps, later called Provence.\n• Infrastructure Development: Romans built extensive road networks, aqueducts, and urban centers.\nRoman Architecture and Engineering\n• Pont du Gard: Magnificent three-tiered aqueduct bridge near Nîmes, built in the 1st century CE.\n• Arena of Nîmes: Well-preserved Roman amphitheater that could hold 24,000 spectators.\n• Theater of Orange: Ancient Roman theater with exceptional acoustics, still used for performances today.\n• Maison Carrée: Perfectly preserved Roman temple in Nîmes, inspired by Greek architecture.\nUrban Development\n• Nemausus (Nîmes): Major Roman city with impressive public buildings and infrastructure.\n• Arausio (Orange): Important Roman settlement with theater and triumphal arch.\n• Arelate (Arles): Significant port city on the Rhône River with amphitheater and circus.\n• Aquae Sextiae (Aix-en-Provence): Founded as a Roman spa town around natural hot springs.",
            "page_number": 3
        },
        {
            "heading": "Medieval Period",
            "content": "The medieval era saw the rise of powerful feudal states, religious influence, and architectural marvels:\nFall of Rome and Barbarian Invasions (5th-6th centuries)\n• Visigothic Kingdom: Germanic tribes established control over much of southern France.\n• Frankish Expansion: Merovingian and later Carolingian rulers gradually extended influence southward.\n• Islamic Incursions: Moorish raids and brief occupation of parts of Provence and Languedoc.\nFeudal Developments\n• County of Provence: Emerged as an independent feudal state with strong ties to the Holy Roman Empire.\n• County of Toulouse: Powerful medieval state controlling much of Languedoc.\n• Cathar Movement: Religious reform movement that flourished in Languedoc during the 12th-13th centuries.\n• Albigensian Crusade (1209-1229): Papal crusade against Cathars that devastated the region.\nArchitectural Heritage\n• Romanesque Churches: Distinctive regional style with thick walls, rounded arches, and sculptural decoration.\n• Gothic Cathedrals: Later medieval churches featuring pointed arches, flying buttresses, and large windows.\n• Fortified Cities: Carcassonne's medieval citadel represents the pinnacle of military architecture.\n• Papal Palace (Avignon): Massive Gothic palace built when the papal court moved to Avignon (1309-1377).",
            "page_number": 6
        },
        {
            "heading": "Renaissance and Early Modern Period",
            "content": "The Renaissance brought cultural renewal, while political upheavals shaped the region's modern identity:\nRenaissance Influence (15th-16th centuries)\n• Italian Cultural Exchange: Close ties with Italian city-states brought Renaissance art and architecture.\n• Château Architecture: Noble families built elegant Renaissance châteaux throughout the region.\n• Humanist Movement: Universities in Montpellier and Toulouse became centers of learning.\n• Protestant Reformation: Significant Protestant communities emerged, leading to religious conflicts.\nWars of Religion (1562-1598)\n• Religious Conflicts: Catholics and Huguenots (Protestants) fought devastating civil wars.\n• Siege of La Rochelle: Major Protestant stronghold that resisted royal authority.\n• Edict of Nantes (1598): Henry IV granted religious tolerance, ending the wars temporarily.\n• Revocation of Edict (1685): Louis XIV's persecution forced many Protestants to flee.\nAbsolutist Monarchy\n• Centralization: French kings gradually reduced regional autonomy and local privileges.\n• Intendant System: Royal administrators imposed central government control.\n• Economic Integration: Improved roads and canals connected the south to Paris and northern France.\n• Cultural Unification: French language and customs gradually replaced regional traditions.",
            "page_number": 9
        },
        {
            "heading": "Modern History",
            "content": "The modern era brought industrialization, tourism, and integration into contemporary France:\nFrench Revolution and Empire (1789-1815)\n• Revolutionary Enthusiasm: The south initially supported revolutionary ideals and constitutional monarchy.\n• Terror Period: Political persecution affected both nobles and clergy in the region.\n• Federalist Revolt: Some southern cities briefly resisted Jacobin centralization.\n• Napoleonic Period: Infrastructure improvements and legal reforms under Napoleon's rule.\n19th Century Developments\n• Industrial Revolution: Coal mining in Alès, textile production, and early manufacturing.\n• Railway Construction: Connection to national rail network facilitated trade and tourism.\n• Agricultural Modernization: Improved viticulture techniques and wine production methods.\n• Urban Growth: Expansion of cities like Marseille, Toulouse, and Montpellier.\n20th Century Transformations\n• World War II: German occupation, Resistance movements, and Liberation campaigns.\n• Economic Modernization: Shift from agriculture to services, technology, and tourism.\n• Regional Identity: Revival of Occitan language and culture, regional political movements.\n• European Integration: Participation in European Union development and Mediterranean cooperation.\nContemporary Challenges\n• Immigration: Significant North African and international immigration since the 1960s.\n• Environmental Concerns: Climate change effects on agriculture, water resources, and coastal areas.\n• Economic Transition: Adaptation to globalization and post-industrial economy.\n• Cultural Preservation: Balancing modernization with protection of historical heritage.",
            "page_number": 12
        }
    ],
    "South of France - Cities.pdf": [
        {
            "heading": "Marseille",
            "content": "France's second-largest city and oldest continuously inhabited city, Marseille is a vibrant Mediterranean metropolis with 2,600 years of history:\nHistorical Significance\n• Founded in 600 BCE by Greek sailors from Phocaea as Massalia.\n• Major trading port connecting France to North Africa and the Eastern Mediterranean.\n• Cultural melting pot with diverse communities from around the Mediterranean basin.\n• European Capital of Culture 2013, highlighting its rich artistic heritage.\nKey Attractions\n• Old Port (Vieux-Port): Historic harbor surrounded by seafood restaurants and boat tours.\n• Basilique Notre-Dame-de-la-Garde: 19th-century basilica offering panoramic city views.\n• MuCEM: Modern museum dedicated to Mediterranean civilizations.\n• Le Panier: Historic neighborhood with narrow streets, artisan shops, and street art.\n• Calanques National Park: Stunning limestone cliffs and hidden coves accessible by boat or hiking.\n• Château d'If: Fortress island made famous by Alexandre Dumas' 'Count of Monte Cristo.'\nNeighborhoods and Districts\n• Le Panier: Oldest district with Marseille's bohemian heart and artistic community.\n• Noailles: Multicultural area known for its African markets and authentic cuisine.\n• Cours Julien: Trendy district with galleries, vintage shops, and vibrant nightlife.\n• Corniche Kennedy: Scenic coastal road with beaches, restaurants, and sea views.\n• Euroméditerranée: Modern business district showcasing contemporary architecture.",
            "page_number": 1
        },
        {
            "heading": "Nice",
            "content": "The jewel of the Côte d'Azur, Nice combines Belle Époque elegance with Mediterranean charm:\nCultural Heritage\n• Capital of the former County of Nice, with strong Italian influences until 1860.\n• Belle Époque architecture reflecting its history as a winter resort for European aristocracy.\n• Birthplace of Henri Matisse and home to an exceptional collection of his works.\n• UNESCO World Heritage Site for its unique urban landscape and architectural ensemble.\nMajor Attractions\n• Promenade des Anglais: Iconic 7-kilometer seafront boulevard lined with palm trees.\n• Vieille Ville (Old Town): Maze of narrow streets with colorful baroque buildings.\n• Musée Matisse: Dedicated to the artist who spent his later years in Nice.\n• Cours Saleya: Famous flower and food market in the heart of the old town.\n• Colline du Château: Hill offering spectacular views over the Baie des Anges.\n• Russian Orthodox Cathedral: Beautiful onion-domed cathedral reflecting Nice's cosmopolitan past.\nBeaches and Coastline\n• Baie des Anges: Sweeping bay with pebble beaches and clear Mediterranean waters.\n• Private Beach Clubs: Luxury establishments offering sun loungers, restaurants, and water sports.\n• Public Beaches: Free access beaches popular with locals and budget-conscious visitors.\n• Water Activities: Swimming, sailing, jet skiing, and paddleboarding opportunities.",
            "page_number": 3
        },
        {
            "heading": "Avignon",
            "content": "The 'City of Popes' is a UNESCO World Heritage Site renowned for its medieval architecture and cultural festivals:\nPpapal History\n• Papal residence from 1309 to 1377 during the Avignon Papacy period.\n• Palais des Papes: Largest Gothic palace in the world, showcasing medieval papal power.\n• Pont Saint-Bénézet: Famous bridge immortalized in the children's song 'Sur le Pont d'Avignon.'\n• Spiritual center that attracted pilgrims and scholars from across Europe.\nArchitectural Marvels\n• Ramparts: Complete 14th-century walls surrounding the historic city center.\n• Cathedral of Our Lady of Doms: Romanesque cathedral adjacent to the papal palace.\n• Place de l'Horloge: Central square with outdoor cafés and the town hall.\n• Petit Palais: Former episcopal palace now housing medieval and Renaissance art.\nCultural Scene\n• Avignon Festival: World-renowned theater festival every July attracting international audiences.\n• Off Festival: Fringe festival featuring experimental and emerging theater companies.\n• Museums: Collection Lambert (contemporary art) and Musée du Petit Palais (medieval art).\n• Street Performers: Year-round entertainment in squares and pedestrian areas.\nGastronomy and Wine\n• Châteauneuf-du-Pape: Nearby wine region producing some of France's most prestigious wines.\n• Local Markets: Weekly markets offering regional specialties and fresh produce.\n• Traditional Restaurants: Establishments serving Provençal cuisine in historic settings.\n• Wine Bars: Venues specializing in Rhône Valley wines and local varietals.",
            "page_number": 5
        },
        {
            "heading": "Toulouse",
            "content": "Known as 'La Ville Rose' (The Pink City) for its distinctive brick architecture, Toulouse is a dynamic university and aerospace center:\nEconomic Powerhouse\n• Aerospace Capital: Home to Airbus headquarters and major aviation industry.\n• Technology Hub: Leading center for space, telecommunications, and information technology.\n• University City: One of France's largest student populations with prestigious institutions.\n• Research Excellence: Major research centers in aerospace, medicine, and biotechnology.\nArchitectural Heritage\n• Brick Gothic: Unique architectural style using local pink terracotta brick.\n• Basilique Saint-Sernin: Largest remaining Romanesque building in Europe.\n• Capitole: Impressive 18th-century city hall dominating the main square.\n• Jacobins Church: Gothic masterpiece with distinctive palm tree vaulting.\n• Canal du Midi: 17th-century canal connecting Toulouse to the Mediterranean.\nCultural Attractions\n• Musée des Augustins: Fine arts museum in a former Gothic convent.\n• Cité de l'Espace: Space-themed park and museum showcasing aerospace achievements.\n• Les Abattoirs: Contemporary art museum in former slaughterhouse buildings.\n• Théâtre du Capitole: Opera house and ballet theater with exceptional acoustics.\nStudent Life and Nightlife\n• University Quarter: Vibrant area around Place Saint-Sernin with cafés and bookshops.\n• Carmes District: Trendy neighborhood with bars, restaurants, and vintage shops.\n• Saint-Cyprien: Left bank district with alternative culture and nightlife.\n• Festivals: Yearly events including Rio Loco world music festival and Printemps de Septembre contemporary art.",
            "page_number": 7
        },
        {
            "heading": "Montpellier",
            "content": "A dynamic university city combining medieval heritage with cutting-edge modernity:\nEducational Excellence\n• University of Montpellier: Founded in 1289, one of Europe's oldest universities.\n• Medical School: Historic faculty of medicine with 800 years of continuous operation.\n• Student Population: Over 70,000 students creating a youthful, energetic atmosphere.\n• Research Centers: Leading institutions in medicine, agriculture, and environmental sciences.\nUrban Development\n• Antigone District: Neoclassical quarter designed by Ricardo Bofill.\n• Modern Tram System: Efficient public transport connecting the city center to suburbs.\n• Port Marianne: New eco-district showcasing sustainable urban planning.\n• Historic Center: Medieval streets centered around Place de la Comédie.\nCultural Offerings\n• Musée Fabre: Exceptional fine arts museum with European paintings and sculptures.\n• Opera Comédie: Historic theater hosting opera, ballet, and classical music.\n• Contemporary Architecture: Innovative buildings like the Courthouse and City Hall annex.\n• Festivals: International events including Radio France Montpellier Festival.\nProximity to Nature\n• Mediterranean Coast: Beaches and seaside resorts just 15 minutes away.\n• Camargue: Unique wetland ecosystem with wild horses and flamingos nearby.\n• Cévennes: Mountain range offering hiking and outdoor activities.\n• Languedoc Vineyards: World-class wine regions within easy reach.",
            "page_number": 9
        }
    ]
}

input_1b = {
    "challenge_info": {
        "challenge_id": "round_1b_002",
        "test_case_name": "travel_planner",
        "description": "France Travel"
    },
    "documents": [
        {
            "filename": "South of France - Cities.pdf",
            "title": "South of France - Cities"
        },
        {
            "filename": "South of France - Cuisine.pdf",
            "title": "South of France - Cuisine"
        },
        {
            "filename": "South of France - History.pdf",
            "title": "South of France - History"
        },
        {
            "filename": "South of France - Restaurants and Hotels.pdf",
            "title": "South of France - Restaurants and Hotels"
        },
        {
            "filename": "South of France - Things to Do.pdf",
            "title": "South of France - Things to Do"
        },
        {
            "filename": "South of France - Tips and Tricks.pdf",
            "title": "South of France - Tips and Tricks"
        },
        {
            "filename": "South of France - Traditions and Culture.pdf",
            "title": "South of France - Traditions and Culture"
        }
    ],
    "persona": {
        "role": "Travel Planner"
    },
    "job_to_be_done": {
        "task": "Suggest a 10-day trip roadmap for a group of 4, emphasizing more on historical places."
    }
}

if __name__ == "__main__":
   print(json.dumps(get_all_content(output_1a),indent=2))