import psycopg2
    
stations_pool = {
    "host": "192.168.178.40",
    "database": "station_data",
    "user": "bahn_miner",
    "password": "bahn_miner_password",
    "port": "5432"
}
timetable_pool = {
    "host": "192.168.178.40",
    "database": "departures_long_distance_stops",
    "user": "bahn_miner",
    "password": "bahn_miner_password",
    "port": "5432"
}
translator = {'Ahlen(Westf)': 'Ahlen (Westf)', 'Alfeld(Leine)': 'Alfeld (Leine)', 'Hamburg-Allermöhe': 'Allermöhe', 'Alsfeld(Oberhess)': 'Alsfeld (Oberhess)', 'Altena(Westf)': 'Altena (Westf)', 'Arnsberg(Westf)': 'Arnsberg (Westf)', 'Ascheberg(Holst)': 'Ascheberg (Holst)', 'Au(Sieg)': 'Au (Sieg)', 'Aßling(Oberbay)': 'Aßling (Oberbay)', 'Babenhausen(Hess)': 'Babenhausen (Hess)', 'Bad Honnef(Rhein)': 'Bad Honnef (Rhein)', 'Bad Münder(Deister)': 'Bad Münder (Deister)', 'Bad Neustadt(Saale)': 'Bad Neustadt (Saale)', 'Bad Soden(Taunus)': 'Bad Soden (Taunus)', 'Hamburg-Bahrenfeld': 'Bahrenfeld', 'Balingen(Württ)': 'Balingen (Württ)', 'Hamburg-Barmbek': 'Barmbek', 'Barnstorf(Han)': 'Barnstorf (Han)', 'Benningen(Neckar)': 'Benningen (Neckar)', 'Bergfelde(b Berlin)': 'Bergfelde (b Berlin)', 'Berlin Attilastr.': 'Berlin Attilastraße', 'Berlin Bornholmer Str.': 'Berlin Bornholmer Straße', 'Berlin Feuerbachstr.': 'Berlin Feuerbachstraße', 'Berlin Greifswalder Str': 'Berlin Greifswalder Straße', 'Berlin Hbf': 'Berlin Hauptbahnhof', 'Berlin-Pichelsberg': 'Berlin Pichelsberg', 'Berlin Poelchaustr.': 'Berlin Poelchaustraße', 'Berlin Raoul-Wallenberg-Str.': 'Berlin Raoul-Wallenberg-Straße', 'Berlin Storkower Str': 'Berlin Storkower Straße', 'Berlin Sundgauer Str': 'Berlin Sundgauer Straße', 'Berlin-Wuhlheide': 'Berlin Wuhlheide', 'Berlin Baumschulenweg': 'Berlin-Baumschulenweg', 'Berlin Westend': 'Berlin-Westend', 'Hamburg Berliner Tor': 'Berliner Tor', 'Bernau(b Berlin)': 'Bernau (b Berlin)', 'Bernau a Chiemsee': 'Bernau a. Chiemsee', 'Betzdorf(Sieg)': 'Betzdorf (Sieg)', 'Biberach(Baden)': 'Biberach (Baden)', 'Biberach(Riß)': 'Biberach (Riß)', 'Bickenbach(Bergstr)': 'Bickenbach (Bergstr)', 'Bietigheim(Baden)': 'Bietigheim (Baden)', 'Hamburg Billwerder-Moorfleet': 'Billwerder-Moorfleet', 'Bingen(Rhein) Hbf': 'Bingen (Rhein) Hbf', 'Bingen(Rhein) Stadt': 'Bingen (Rhein) Stadt', 'Birkenwerder(b Berlin)': 'Birkenwerder (b Berlin)', 'Blankenburg(Harz)': 'Blankenburg (Harz)', 'Hamburg-Blankenese': 'Blankenese', 'Bondorf(b Herrenberg)': 'Bondorf (b Herrenberg)', 'Borken(Hess)': 'Borken (Hess)', 'Borsdorf(Sachs)': 'Borsdorf (Sachs)', 'Brake(b Bielefeld)': 'Brake (b Bielefeld)', 'Buchenau(Oberbay)': 'Buchenau (Oberbay)', 'Buchholz(Nordheide)': 'Buchholz (Nordheide)', 'Bullay(DB)': 'Bullay (DB)', 'Burgau(Schwab)': 'Burgau (Schwab)', 'Böbingen(Rems)': 'Böbingen (Rems)', 'Bühl(Baden)': 'Bühl (Baden)', 'Bünde(Westf)': 'Bünde (Westf)', 'Calbe(Saale) Ost': 'Calbe (Saale) Ost', 'Celle': 'Celle Pbf', 'Cham(Oberpf)': 'Cham (Oberpf)', 'Cochem(Mosel)': 'Cochem (Mosel)', 'Coesfeld(Westf)': 'Coesfeld (Westf)', 'Coswig(b Dresden)': 'Coswig (b Dresden)', 'Creußen(Oberfr)': 'Creußen (Oberfr)', 'Dettingen(Main)': 'Dettingen (Main)', 'Hamburg Diebsteich': 'Diebsteich', 'Diedorf(Schwab)': 'Diedorf (Schwab)', 'Dietzenbach Mitte': 'Dietzenbach-Mitte', 'Dillingen(Donau)': 'Dillingen (Donau)', 'Dillingen(Saar)': 'Dillingen (Saar)', 'Duisburg-Schlenk': 'Duisburg Schlenk', 'Düsseldorf Völklinger Str.': 'Düsseldorf Völklinger Straße', 'Düsseldorf-Zoo': 'Düsseldorf Zoo', 'Düsseldorf Friedrichstadt': 'Düsseldorf-Friedrichstadt', 'Ebenhausen(Unterfr)': 'Ebenhausen (Unterfr)', 'Ebersbach(Fils)': 'Ebersbach (Fils)', 'Ebersbach(Sachs)': 'Ebersbach (Sachs)', 'Ebersberg(Oberbay)': 'Ebersberg (Oberbay)', 'Egestorf(Deister)': 'Egestorf (Deister)', 'Ehingen(Donau)': 'Ehingen (Donau)', 'Ehningen(b Böblingen)': 'Ehningen (b Böblingen)', 'Eichenau(Oberbay)': 'Eichenau (Oberbay)', 'Hamburg-Eidelstedt': 'Eidelstedt', 'Eilsleben(b Magdeburg)': 'Eilsleben (b Magdeburg)', 'Eislingen(Fils)': 'Eislingen (Fils)', 'Hamburg Elbbrücken': 'Elbbrücken', 'Hamburg Elbgaustraße': 'Elbgaustraße', 'Ellingen(Bay)': 'Ellingen (Bay)', 'Elze(Han)': 'Elze (Han)', 'Erbach(Württ)': 'Erbach (Württ)', 'Erzingen(Baden)': 'Erzingen (Baden)', 'Esslingen(Neckar)': 'Esslingen (Neckar)', 'Eutingen(Baden)': 'Eutingen (Baden)', 'Falkenberg(Elster)': 'Falkenberg (Elster)', 'Feldkirchen(b München)': 'Feldkirchen (b München)', 'Finsterwalde(Niederlausitz)': 'Finsterwalde (Niederlausitz)', 'Flörsheim(Main)': 'Flörsheim (Main)', 'Forchheim(Oberfr)': 'Forchheim (Oberfr)', 'Forchheim(b Karlsruhe)': 'Forchheim (b Karlsruhe)', 'Frankfurt(M)Galluswarte': 'Frankfurt (Main) Galluswarte', 'Frankfurt(M)Hauptwache': 'Frankfurt (Main) Hauptwache', 'Frankfurt(Main)Hbf': 'Frankfurt (Main) Hbf', 'Frankfurt(M)Konstablerwache': 'Frankfurt (Main) Konstablerwache', 'Frankfurt(M)Lokalbahnhof': 'Frankfurt (Main) Lokalbahnhof', 'Frankfurt(M)Mühlberg': 'Frankfurt (Main) Mühlberg', 'Frankfurt(Main)Ost': 'Frankfurt (Main) Ost', 'Frankfurt(M)Ostendstraße': 'Frankfurt (Main) Ostendstraße', 'Frankfurt(M)Stresemannallee': 'Frankfurt (Main) Stresemannallee', 'Frankfurt(Main)Süd': 'Frankfurt (Main) Süd', 'Frankfurt(M)Taunusanlage': 'Frankfurt (Main) Taunusanlage', 'Frankfurt(Main)West': 'Frankfurt (Main) West', 'Frankfurt(Oder)': 'Frankfurt (Oder)', 'Frankfurt(Main)Messe': 'Frankfurt am Main Messe', 'Fredersdorf(b Berlin)': 'Fredersdorf (b Berlin)', 'Freiberg(Neckar)': 'Freiberg (Neckar)', 'Freiberg(Sachs)': 'Freiberg (Sachs)', 'Freiburg(Breisgau) Hbf': 'Freiburg (Breisgau) Hbf', 'Friedberg(Hess)': 'Friedberg (Hess)', 'Hamburg Friedrichsberg': 'Friedrichsberg', 'Friedrichsdorf(Taunus)': 'Friedrichsdorf (Taunus)', 'Friedrichsfeld(Niederrhein)': 'Friedrichsfeld (Niederrhein)', 'Furth(b Deisenhofen)': 'Furth (b Deisenhofen)', 'Fürstenberg(Havel)': 'Fürstenberg (Havel)', 'Fürstenwalde(Spree)': 'Fürstenwalde (Spree)', 'Fürth(Bay)Hbf': 'Fürth (Bay) Hbf', 'Geislingen(Steige)': 'Geislingen (Steige)', 'Gemünden(Main)': 'Gemünden (Main)', 'Giengen(Brenz)': 'Giengen (Brenz)', 'Glauchau(Sachs)': 'Glauchau (Sachs)', 'Gronau(Westf)': 'Gronau (Westf)', 'Groß-Rohrheim': 'Groß Rohrheim', 'Großauheim(Kr Hanau)': 'Großauheim (Kr Hanau)', 'Grub(Oberbay)': 'Grub (Oberbay)', 'Grünberg(Oberhess)': 'Grünberg (Oberhess)', 'Halle(Saale)Hbf': 'Halle (Saale) Hbf', 'Hallstadt(b Bamberg)': 'Hallstadt (b Bamberg)', 'Hamm(Westf)Hbf': 'Hamm (Westf) Hbf', 'Hamburg-Hammerbrook': 'Hammerbrook', 'Hannover-Ledeburg': 'Hannover - Ledeburg', 'Hannover-Vinnhorst': 'Hannover - Vinnhorst', 'Hannover Bismarckstr.': 'Hannover Bismarckstraße', 'Hannover Flughafen': 'Hannover-Flughafen', 'Hamburg-Harburg Rathaus': 'Harburg Rathaus', 'Hamburg Hasselbrook': 'Hasselbrook', 'Hattersheim(Main)': 'Hattersheim (Main)', 'Hattingen(Ruhr)': 'Hattingen (Ruhr)', 'Haßloch(Pfalz)': 'Haßloch (Pfalz)', 'Heide(Holst)': 'Heide (Holst)', 'Heidelberg Orthopädie': 'Heidelberg-Orthopädie', 'Heidesheim(Rheinhess)': 'Heidesheim (Rheinhess)', 'Heimersheim/Lohrsdorf': 'Heimersheim / Lohrsdorf', 'Hamburg-Heimfeld': 'Heimfeld', 'Hennef(Sieg)': 'Hennef (Sieg)', 'Hennigsdorf(b Berlin)': 'Hennigsdorf (b Berlin)', 'Heppenheim(Bergstr)': 'Heppenheim (Bergstr)', 'Herborn(Dillkr)': 'Herborn (Dillkr)', 'Herten(Westf)': 'Herten (Westf)', 'Herzberg(Harz)': 'Herzberg (Harz)', 'Hirschhorn(Neckar)': 'Hirschhorn (Neckar)', 'Hochheim(Main)': 'Hochheim (Main)', 'Hamburg Hochkamp': 'Hochkamp', 'Hofheim(Taunus)': 'Hofheim (Taunus)', 'Hohen Neuendorf(b Berlin)': 'Hohen Neuendorf (b Berlin)', 'Hamburg Hoheneichen': 'Hoheneichen', 'Hamburg Holstenstraße': 'Holstenstraße', 'Homburg(Saar)Hbf': 'Homburg (Saar) Hbf', 'Hoppegarten(Mark)': 'Hoppegarten (Mark)', 'Idstein(Taunus)': 'Idstein (Taunus)', 'Illingen(Württ)': 'Illingen (Württ)', 'Hamburg Jungfernstieg': 'Jungfernstieg', 'Kahl(Main)': 'Kahl (Main)', 'Kahla(Thür)': 'Kahla (Thür)', 'Karlstadt(Main)': 'Karlstadt (Main)', 'Kempten(Allgäu)Hbf': 'Kempten (Allgäu) Hbf', 'Kirchhain(Bz Kassel)': 'Kirchhain (Bz Kassel)', 'Kirchheim(Neckar)': 'Kirchheim (Neckar)', 'Kirchheim(Teck)': 'Kirchheim (Teck)', 'Kirchheim(Teck)-Ötlingen': 'Kirchheim (Teck)-Ötlingen', 'Hamburg Klein Flottbek': 'Klein Flottbek', 'Kronberg(Taunus)': 'Kronberg (Taunus)', 'Köln Geldernstr./Parkgürtel': 'Köln-Geldernstr./Parkgürtel', 'Hamburg Königstraße': 'Königstraße', 'Lage(Lippe)': 'Lage (Lippe)', 'Lahr(Schwarzw)': 'Lahr (Schwarzw)', 'Lambrecht(Pfalz)': 'Lambrecht (Pfalz)', 'Landau(Isar)': 'Landau (Isar)', 'Landau(Pfalz)Hbf': 'Landau (Pfalz) Hbf', 'Landshut(Bay)Hbf': 'Landshut (Bay) Hbf', 'Hamburg Landungsbrücken': 'Landungsbrücken', 'Hamburg Landwehr': 'Landwehr', 'Langebrück(Sachs)': 'Langebrück (Sachs)', 'Langen(Hess)': 'Langen (Hess)', 'Langenau(Württ)': 'Langenau (Württ)', 'Hamburg-Langenfelde': 'Langenfelde', 'Langenhagen-Kaltenweide': 'Langenhagen - Kaltenweide', 'Langenhagen Mitte': 'Langenhagen-Mitte', 'Langenhorn(Schlesw)': 'Langenhorn (Schlesw)', 'Langweid(Lech)': 'Langweid (Lech)', 'Laudenbach(Bergstr)': 'Laudenbach (Bergstr)', 'Lauf(links Pegnitz)': 'Lauf (links Pegnitz)', 'Lauf(rechts Pegnitz)': 'Lauf (rechts Pegnitz)', 'Lauffen(Neckar)': 'Lauffen (Neckar)', 'Leer(Ostfriesl)': 'Leer (Ostfriesl)', 'Lengerich(Westf)': 'Lengerich (Westf)', 'Leutesdorf(Rhein)': 'Leutesdorf (Rhein)', 'Lich(Oberhess)': 'Lich (Oberhess)', 'Limburg(Lahn)': 'Limburg (Lahn)', 'Lingen(Ems)': 'Lingen (Ems)', 'Linz(Rhein)': 'Linz (Rhein)', 'Lorch(Württ)': 'Lorch (Württ)', 'Ludwigshafen(Rhein) Mitte': 'Ludwigshafen (Rhein) Mitte', 'Luisenthal(Saar)': 'Luisenthal (Saar)', 'Löbau(Sachs)': 'Löbau (Sachs)', 'Löhne(Westf)': 'Löhne (Westf)', 'Löwenberg(Mark)': 'Löwenberg (Mark)', 'Lübben(Spreewald)': 'Lübben (Spreewald)', 'Lübbenau(Spreewald)': 'Lübbenau (Spreewald)', 'Lünen-Preußen': 'Lünen Preußen', 'Marbach(Neckar)': 'Marbach (Neckar)', 'Marburg(Lahn)': 'Marburg (Lahn)', 'Markdorf(Baden)': 'Markdorf (Baden)', 'Menden(Rheinl)': 'Menden (Rheinl)', 'Merzig(Saar)': 'Merzig (Saar)', 'Metzingen(Württ)': 'Metzingen (Württ)', 'Minden(Westf)': 'Minden (Westf)', 'Hamburg Mittlerer Landweg': 'Mittlerer Landweg', 'Mosbach(Baden)': 'Mosbach (Baden)', 'Mühlhausen(Thür)': 'Mühlhausen (Thür)', 'Mühlheim(Main)': 'Mühlheim (Main)', 'Mülheim(Ruhr)Hbf': 'Mülheim (Ruhr) Hbf', 'Mülheim(Ruhr)West': 'Mülheim (Ruhr) West', 'München Leienfelsstr.': 'München Leienfelsstraße', 'München Hackerbrücke': 'München-Hackerbrücke', 'München Hirschgarten': 'München-Hirschgarten', 'München-Laim': 'München-Laim Pbf', 'München-Riem': 'München-Riem Pbf', 'Münster(Westf)Hbf': 'Münster (Westf) Hbf', 'Naumburg(Saale)Hbf': 'Naumburg (Saale) Hbf', 'Hamburg-Nettelnburg': 'Nettelnburg', 'Neu-Isenburg': 'Neu Isenburg', 'Neubrücke(Nahe)': 'Neubrücke (Nahe)', 'Neuburg(Donau)': 'Neuburg (Donau)', 'Neufahrn(Niederbay)': 'Neufahrn (Niederbay)', 'Neufahrn(b Freising)': 'Neufahrn (b Freising)', 'Neuhaus(Pegnitz)': 'Neuhaus (Pegnitz)', 'Neuhof(Kr Fulda)': 'Neuhof (Kr Fulda)', 'Neukirchen(b Sulzb)': 'Neukirchen (b Sulzb)', 'Neumarkt(Oberpf)': 'Neumarkt (Oberpf)', 'Neunkirchen(Saar)Hbf': 'Neunkirchen (Saar) Hbf', 'Neunkirchen(Saar)-Wellesweiler': 'Neunkirchen (Saar)-Wellesweiler', 'Neustadt(Aisch)Bahnhof': 'Neustadt (Aisch) Bahnhof', 'Neustadt(Kr Marburg)': 'Neustadt (Kr Marburg)', 'Neustadt(Schwarzw)': 'Neustadt (Schwarzw)', 'Neustadt(Weinstr)Hbf': 'Neustadt (Weinstr) Hbf', 'Hamburg Neuwiedenthal': 'Neuwiedenthal', 'Neuwirtshaus(Porscheplatz)': 'Neuwirtshaus (Porscheplatz)', 'Niedernhausen(Taunus)': 'Niedernhausen (Taunus)', 'Nienburg(Weser)': 'Nienburg (Weser)', 'Northeim(Han)': 'Northeim (Han)', 'Nürnberg Rothenburger Str.': 'Nürnberg Rothenburger Straße', 'Nürnberg Frankenstadion': 'Nürnberg-Frankenstadion', 'Nürnberg Ostring': 'Nürnberg-Ostring', 'Oberndorf(Neckar)': 'Oberndorf (Neckar)', 'Oberursel(Taunus)': 'Oberursel (Taunus)', 'Offenbach(Main)Hbf': 'Offenbach (Main) Hbf', 'Offenbach(Main) Kaiserlei': 'Offenbach (Main) Kaiserlei', 'Offenbach(Main) Ledermuseum': 'Offenbach (Main) Ledermuseum', 'Offenbach(Main) Marktplatz': 'Offenbach (Main) Marktplatz', 'Offenbach(Main)Ost': 'Offenbach (Main) Ost', 'Hamburg-Ohlsdorf': 'Ohlsdorf', 'Oldenburg(Oldb)Hbf': 'Oldenburg (Oldb) Hbf', 'Ostheim(b Butzbach)': 'Ostheim (b Butzbach)', 'Hamburg-Othmarschen': 'Othmarschen', 'Hamburg-Ottensen': 'Ottensen', 'Ottersberg(Han)': 'Ottersberg (Han)', 'Ottweiler(Saar)': 'Ottweiler (Saar)', 'Papenburg(Ems)': 'Papenburg (Ems)', 'Pfaffenhofen(Ilm)': 'Pfaffenhofen (Ilm)', 'Philippsburg(Baden)': 'Philippsburg (Baden)', 'Plaue(Thür)': 'Plaue (Thür)', 'Plauen(Vogtl) ob Bf': 'Plauen (Vogtl) ob Bf', 'Hamburg-Poppenbüttel': 'Poppenbüttel', 'Porz(Rhein)': 'Porz (Rhein)', 'Pulling(b Freising)': 'Pulling (b Freising)', 'Radldorf(Niederbay)': 'Radldorf (Niederbay)', 'Hamburg Reeperbahn': 'Reeperbahn', 'Reichenbach(Fils)': 'Reichenbach (Fils)', 'Reichenbach(Vogtl) ob Bf': 'Reichenbach (Vogtl) ob Bf', 'Reinfeld(Holst)': 'Reinfeld (Holst)', 'Rheinfelden(Baden)': 'Rheinfelden (Baden)', 'Hamburg-Rissen': 'Rissen', 'Rohrbach(Ilm)': 'Rohrbach (Ilm)', 'Rohrbach(Saar)': 'Rohrbach (Saar)', 'Rosbach(Sieg)': 'Rosbach (Sieg)', 'Rostock-Evershagen': 'Rostock Evershagen', 'Rostock-Lichtenhagen': 'Rostock Lichtenhagen', 'Rotenburg(Wümme)': 'Rotenburg (Wümme)', 'Hamburg-Rothenburgsort': 'Rothenburgsort', 'Rottenburg(Neckar)': 'Rottenburg (Neckar)', 'Roßlau(Elbe)': 'Roßlau (Elbe)', 'Rudolstadt(Thür)': 'Rudolstadt (Thür)', 'Röthenbach(Pegnitz)': 'Röthenbach (Pegnitz)', 'Hamburg Rübenkamp': 'Rübenkamp', 'Rüdesheim(Rhein)': 'Rüdesheim (Rhein)', 'Saalfeld(Saale)': 'Saalfeld (Saale)', 'Saarburg(Bz Trier)': 'Saarburg (Bz Trier)', 'Sandersleben(Anh)': 'Sandersleben (Anh)', 'Scheidt(Saar)': 'Scheidt (Saar)', 'Schladern(Sieg)': 'Schladern (Sieg)', 'Schwalbach(Taunus)Limes': 'Schwalbach (Taunus) Limes', 'Schweich(DB)': 'Schweich (DB)', 'Schwerte(Ruhr)': 'Schwerte (Ruhr)', 'Schönebeck(Elbe)': 'Schönebeck (Elbe)', 'Schönefeld(bei Berlin)': 'Schönefeld (bei Berlin)', 'Seelze': 'Seelze Pbf', 'Singen(Hohentwiel)': 'Singen (Hohentwiel)', 'Sinsheim(Elsenz) Hbf': 'Sinsheim (Elsenz) Hbf', 'Sinzig(Rhein)': 'Sinzig (Rhein)', 'Soltau(Han)': 'Soltau (Han)', 'Sonneberg(Thür)Hbf': 'Sonneberg (Thür) Hbf', 'St Goar': 'St. Goar', 'St Ingbert': 'St. Ingbert', 'St Michaelisdonn': 'St. Michaelisdonn', 'St Wendel': 'St. Wendel', 'Stadt Wehlen(Sachs)': 'Stadt Wehlen (Sachs)', 'Hamburg Stadthausbrücke': 'Stadthausbrücke', 'Starnberg Nord': 'Starnberg-Nord', 'Steinau(Straße)': 'Steinau (Straße)', 'Hamburg-Stellingen': 'Stellingen', 'Hamburg-Sternschanze': 'Sternschanze', 'Stolberg(Rheinl)Hbf': 'Stolberg (Rheinl) Hbf', 'Stuttgart Nürnberger Str.': 'Stuttgart Nürnberger Straße', 'Stuttgart Schwabstr.': 'Stuttgart Schwabstraße', 'Stuttgart-Österfeld': 'Stuttgart Österfeld', 'Stuttgart-Untertürkheim': 'Stuttgart-Untertürkheim Pbf', 'Sulz(Neckar)': 'Sulz (Neckar)', 'Sulzbach(Murr)': 'Sulzbach (Murr)', 'Sulzbach(Saar)': 'Sulzbach (Saar)', 'Hamburg-Sülldorf': 'Sülldorf', 'Tamm(Württ)': 'Tamm (Württ)', 'Hamburg-Tiefstack': 'Tiefstack', 'Tiengen(Hochrhein)': 'Tiengen (Hochrhein)', 'Urbach(b Schorndorf)': 'Urbach (b Schorndorf)', 'Vaihingen(Enz)': 'Vaihingen (Enz)', 'Varel(Oldb)': 'Varel (Oldb)', 'Hamburg-Veddel': 'Veddel', 'Velten(Mark)': 'Velten (Mark)', 'Verden(Aller)': 'Verden (Aller)', 'Villingen(Schwarzw)': 'Villingen (Schwarzw)', 'Vilshofen(Niederbay)': 'Vilshofen (Niederbay)', 'Voerde(Niederrhein)': 'Voerde (Niederrhein)', 'Wabern(Bz Kassel)': 'Wabern (Bz Kassel)', 'Walldorf(Hess)': 'Walldorf (Hess)', 'Hamburg Wandsbeker Chaussee': 'Wandsbeker Chaussee', 'Wangen(Allgäu)': 'Wangen (Allgäu)', 'Warburg(Westf)': 'Warburg (Westf)', 'Waren(Müritz)': 'Waren (Müritz)', 'Wedel(Holst)': 'Wedel (Holst)', 'Weiden(Oberpf)': 'Weiden (Oberpf)', 'Weiler(Rems)': 'Weiler (Rems)', 'Weilheim(Oberbay)': 'Weilheim (Oberbay)', 'Weinheim(Bergstr)Hbf': 'Weinheim (Bergstr) Hbf', 'Weißenburg(Bay)': 'Weißenburg (Bay)', 'Weißwasser(Oberlausitz)': 'Weißwasser (Oberlausitz)', 'Hamburg-Wellingsbüttel': 'Wellingsbüttel', 'Wendlingen(Neckar)': 'Wendlingen (Neckar)', 'Wennigsen(Deister)': 'Wennigsen (Deister)', 'Werder(Havel)': 'Werder (Havel)', 'Wernau(Neckar)': 'Wernau (Neckar)', 'Westerland(Sylt)': 'Westerland (Sylt)', 'Westheim(Schwab)': 'Westheim (Schwab)', 'Wetter(Ruhr)': 'Wetter (Ruhr)', 'Weßling(Oberbay)': 'Weßling (Oberbay)', 'Wickede(Ruhr)': 'Wickede (Ruhr)', 'Wiesau(Oberpf)': 'Wiesau (Oberpf)', 'Hamburg-Wilhelmsburg': 'Wilhelmsburg', 'Winden(Pfalz)': 'Winden (Pfalz)', 'Winsen(Luhe)': 'Winsen (Luhe)', 'Winterbach(b Schorndorf)': 'Winterbach (b Schorndorf)', 'Wissen(Sieg)': 'Wissen (Sieg)', 'Wolfen(Bitterfeld)': 'Wolfen (Bitterfeld)', 'Wörth(Isar)': 'Wörth (Isar)', 'Wörth(Rhein)': 'Wörth (Rhein)', 'Wünsdorf-Waldstadt': 'Wünsdorf Waldstadt', 'Zwickau(Sachs)Hbf': 'Zwickau (Sachs) Hbf', 'Zwingenberg(Bergstr)': 'Zwingenberg (Bergstr)'}
translator.update({
    'Rückersdorf(Mfr)': 'Rückersdorf (Mittelfr)',
    # 'Taucha(Leipzig)': 'Taucha (b Leipzig)',
    # 'Zepernick(Bernau)': 'Zepernick (b Bernau)',
    'Weilimdorf': 'Stuttgart-Weilimdorf',
    'Schwarzenfeld(Opf)': 'Schwarzenfeld (Oberpf)',
    'St Georgen(Schwarzw)': 'St. Georgen (Schwarzw)',
    'St Ilgen-Sandhausen': 'St. Ilgen/Sandhausen',
    'Steinach(bei Rothenburg ob der Tauber)': 'Steinach (b Rothenburg o.d. Tauber)',
    'Steinbach am Wald': 'Steinbach a Wald',
    'Uffing a Staffelsee': 'Uffing am Staffelsee',
    'Völksen/Eldagsen': 'Völksen-Eldagsen',
    'Wuppertal-Zoologischer Garten': 'Wuppertal Zoologischer Garten',
    "Türkheim(Bay)Bf": "Türkheim (Bay)",
    "Steinheim(Main)": "Steinheim am Main (Hanau)",
    'Ahlten': 'Ahlten (Han)',
    # 'Arnsdorf(Dresden)': 'Arnsdorf (b Dresden)',
    'Bad Münster a Stein': 'Bad Münster am Stein',
    'Baden(Verden)': 'Baden (Kr Verden)',
    'Berlin Alt-Reinickendorf': 'Berlin Alt Reinickendorf', 
    'Berlin Anhalter Bf': 'Berlin Anhalter Bahnhof', 
    'Berlin Betriebsbf Rummelsburg': 'Berlin-Rummelsburg Betriebsbahnhof', 
    'Berlin Messe Nord/ZOB (Witzleben)': 'Berlin Messe Nord/ZOB', 
    'Berlin Yorckstr.(S1)': 'Berlin Yorckstraße/Großgörschenstraße', 
    'Berlin Yorckstr.(S2)': 'Berlin Yorckstraße', 
    'Berlin-Tegel (S)': 'Berlin-Tegel', 
    'Blankenfelde(Teltow-Fläming)': 'Blankenfelde (Kr Teltow-Fläming)',
    # 'Borna(Leipzig)': 'Borna (b Leipzig)', 
    # 'Burg(Magdeburg)': 'Burg (b Magdeburg)', 
    'Burgdorf': 'Burgdorf (Han)', 
    'Calau(Nl)': 'Calau (Niederlausitz)', 
    'Dedensen-Gümmer': 'Dedensen / Gümmer', 
    'Ennepetal': 'Ennepetal (Gevelsberg)', 
    # 'Fischbach(Nürnberg)', 
    'Frankfurt am Main - Stadion': 'Frankfurt (Main) Stadion', 
    'Frankfurt(M) Flughafen Fernbf': 'Frankfurt am Main Flughafen Fernbahnhof', 
    'Frankfurt(M) Flughafen Regionalbf': 'Frankfurt (Main) Flughafen Regionalbahnhof', 
    'Frankfurt(Main)-Gateway Gardens': 'Frankfurt am Main Gateway Gardens', 
    # 'Friedberg(Augsburg)', 
    'Friedrich Wilhelmshütte': 'Friedrich-Wilhelms-Hütte', 
    'Goldberg(Württ)': 'Goldberg', 
    'Groß-Umstadt Wiebelsbach': 'Groß Umstadt-Wiebelsbach', 
    'Großhesselohe Isartalbf': 'Großhesselohe Isartalbahnhof',
    'Gummersbach-Dieringhausen': 'Dieringhausen', 
    'Gundelfingen(Breisgau)': 'Gundelfingen', 
    'Hamburg Airport': 'Hamburg Airport (Flughafen)', 
    'Hamburg Alte Wöhr': 'Alte Wöhr (Stadtpark)', 
    'Hamburg Kornweg(Klein Borstel)': 'Kornweg (Klein Borstel)',
    'Hannover Anderten-Misburg': 'Anderten-Misburg', 
    'Hannover Messe/Laatzen': 'Hannover-Messe / Laatzen', 
    'Haste': 'Haste (Han)', 
    'Heidelberg-Schlierbach/Ziegelhausen': 'Heidelberg-Schlierbach-Ziegelhausen', 
    'Heidelberg-Weststadt/Südstadt': 'HD-Weststadt/Südstadt', 
    'Hennef im Siegbogen': 'Hennef Im Siegbogen',
    'Herbolzheim(Breisg)': 'Herbolzheim (Breisgau)', 
    'Hersbruck(r Pegnitz)': 'Hersbruck (rechts Pegnitz)', 
    'Hornberg(Schwarzw)': 'Hornberg', 
    'Immenhausen': 'Immenhausen (Hess)', 
    'Königstein(Sächs Schw)': 'Königstein (Sächs Schweiz)', 
    'Langenfeld(Rhld)': 'Langenfeld (Rheinl)', 
    'Langenfeld(Rhld)-Berghausen': 'Langenfeld (Rheinl)-Berghausen', 
    'Leipzig/Halle Flughafen': 'Flughafen Leipzig/Halle',
    'Ludwigshafen(Rh)Hbf': 'Ludwigshafen (Rhein) Hbf',
    'Mannheim ARENA/Maimarkt': 'Mannheim ARENA / Maimarkt', 
    'Meckenheim(Bz Köln)': 'Meckenheim', 
    'Morsum': 'Morsum (Sylt)', 
    'Mühlheim(Main)-Dietesheim': 'Mühlheim-Dietesheim', 
    'Mülheim(Ruhr)Styrum': 'Mülheim (Ruhr)-Styrum', 
    'München Flughafen Besucherpark': 'Flughafen München Besucherpark', 
    'München Flughafen Terminal': 'Flughafen München', 
    'München St.Martin-Str.': 'München St Martin Straße',
    'Münster(W)Zentrum Nord': 'Münster Zentrum Nord', 
    'Neustadt am Rübenberge': 'Neustadt a Rübenberge', 
    'Obertshausen(Kr Of)': 'Obertshausen (Kr Offenbach)', 
    'Osterhofen(Nby)': 'Osterhofen (Niederbay)', 
    'Petershausen(Obb)': 'Petershausen (Oberbay)', 
    'Planegg': 'Planegg (Krailling)', 
    'Potsdam-Babelsberg': 'Babelsberg', 
    'Rodenbach(b Hanau)': 'Rodenbach bei Hanau', 
    'Ronnenberg': 'Ronnenberg (Han)', 
    'Rostock-Lütten Klein': 'Rostock Lütten Klein', 
    'Sechtem': 'Bornheim-Sechtem'
})
translator.update({'Arnsdorf(Dresden)': 'Arnsdorf (b Dresden)', 'Borna(Leipzig)': 'Borna (b Leipzig)', 'Burg(Magdeburg)': 'Burg (b Magdeburg)', 'Fischbach(Nürnberg)': 'Fischbach (b Nürnberg)', 'Frankfurt-Ginnheim': 'Frankfurt (Main) Ginnheim', 'Frankfurt-Niederrad': 'Frankfurt (Main) Niederrad', 'Friedberg(Augsburg)': 'Friedberg (b Augsburg)', 'Taucha(Leipzig)': 'Taucha (b Leipzig)', 'Zepernick(Bernau)': 'Zepernick (b Bernau)'})


def print_list(list):
    for el in list:
        print(el)

class pg_query_handler:
    def __init__(self):
        self.st_client = psycopg2.connect(**stations_pool)
        self.st_cursor = self.st_client.cursor()
        self.tt_client = psycopg2.connect(**timetable_pool)
        self.tt_cursor = self.tt_client.cursor()
        
    def get_station_data(self, station_name):
        self.st_cursor.execute(
            '''
            with station as (
                select id, name from stations
                where name = '{station_name}'
            ),
            eva as (
                select station_id, number, latitude, longitude from eva_numbers
                where eva_numbers.station_id = (select id from station limit 1) and
                    eva_numbers.is_main is true
            )
            select name, latitude, longitude from station
            join eva on station.id = eva.station_id
            ;'''.format(station_name=station_name))
        result = self.st_cursor.fetchall()
        return result
    
    def get_non_matching_names(self):
        tt_names = ['Ahlen(Westf)', 'Ahlten', 'Alfeld(Leine)', 'Alsfeld(Oberhess)', 'Altena(Westf)', 'Arnsberg(Westf)', 'Arnsdorf(Dresden)', 'Ascheberg(Holst)', 'Au(Sieg)', 'Aßling(Oberbay)', 'Babenhausen(Hess)', 'Bad Honnef(Rhein)', 'Bad Münder(Deister)', 'Bad Münster a Stein', 'Bad Neustadt(Saale)', 'Bad Soden(Taunus)', 'Baden(Verden)', 'Balingen(Württ)', 'Barnstorf(Han)', 'Benningen(Neckar)', 'Bergfelde(b Berlin)', 'Berlin Alt-Reinickendorf', 'Berlin Anhalter Bf', 'Berlin Attilastr.', 'Berlin Baumschulenweg', 'Berlin Betriebsbf Rummelsburg', 'Berlin Bornholmer Str.', 'Berlin Feuerbachstr.', 'Berlin Greifswalder Str', 'Berlin Hbf', 'Berlin Messe Nord/ZOB (Witzleben)', 'Berlin Poelchaustr.', 'Berlin Raoul-Wallenberg-Str.', 'Berlin Storkower Str', 'Berlin Sundgauer Str', 'Berlin Westend', 'Berlin Yorckstr.(S1)', 'Berlin Yorckstr.(S2)', 'Berlin-Pichelsberg', 'Berlin-Tegel (S)', 'Berlin-Wuhlheide', 'Bernau a Chiemsee', 'Bernau(b Berlin)', 'Betzdorf(Sieg)', 'Biberach(Baden)', 'Biberach(Riß)', 'Bickenbach(Bergstr)', 'Bietigheim(Baden)', 'Bingen(Rhein) Hbf', 'Bingen(Rhein) Stadt', 'Birkenwerder(b Berlin)', 'Blankenburg(Harz)', 'Blankenfelde(Teltow-Fläming)', 'Bondorf(b Herrenberg)', 'Borken(Hess)', 'Borna(Leipzig)', 'Borsdorf(Sachs)', 'Brake(b Bielefeld)', 'Buchenau(Oberbay)', 'Buchholz(Nordheide)', 'Bullay(DB)', 'Burg(Magdeburg)', 'Burgau(Schwab)', 'Burgdorf', 'Böbingen(Rems)', 'Bühl(Baden)', 'Bünde(Westf)', 'Calau(Nl)', 'Calbe(Saale) Ost', 'Celle', 'Cham(Oberpf)', 'Cochem(Mosel)', 'Coesfeld(Westf)', 'Coswig(b Dresden)', 'Creußen(Oberfr)', 'Dedensen-Gümmer', 'Dettingen(Main)', 'Diedorf(Schwab)', 'Dietzenbach Mitte', 'Dillingen(Donau)', 'Dillingen(Saar)', 'Duisburg-Schlenk', 'Düsseldorf Friedrichstadt', 'Düsseldorf Völklinger Str.', 'Düsseldorf-Zoo', 'Ebenhausen(Unterfr)', 'Ebersbach(Fils)', 'Ebersbach(Sachs)', 'Ebersberg(Oberbay)', 'Egestorf(Deister)', 'Ehingen(Donau)', 'Ehningen(b Böblingen)', 'Eichenau(Oberbay)', 'Eilsleben(b Magdeburg)', 'Eislingen(Fils)', 'Ellingen(Bay)', 'Elze(Han)', 'Ennepetal', 'Erbach(Württ)', 'Erzingen(Baden)', 'Esslingen(Neckar)', 'Eutingen(Baden)', 'Falkenberg(Elster)', 'Feldkirchen(b München)', 'Finsterwalde(Niederlausitz)', 'Fischbach(Nürnberg)', 'Flörsheim(Main)', 'Forchheim(Oberfr)', 'Forchheim(b Karlsruhe)', 'Frankfurt am Main - Stadion', 'Frankfurt(M) Flughafen Fernbf', 'Frankfurt(M) Flughafen Regionalbf', 'Frankfurt(M)Galluswarte', 'Frankfurt(M)Hauptwache', 'Frankfurt(M)Konstablerwache', 'Frankfurt(M)Lokalbahnhof', 'Frankfurt(M)Mühlberg', 'Frankfurt(M)Ostendstraße', 'Frankfurt(M)Stresemannallee', 'Frankfurt(M)Taunusanlage', 'Frankfurt(Main)-Gateway Gardens', 'Frankfurt(Main)Hbf', 'Frankfurt(Main)Messe', 'Frankfurt(Main)Ost', 'Frankfurt(Main)Süd', 'Frankfurt(Main)West', 'Frankfurt(Oder)', 'Frankfurt-Ginnheim', 'Frankfurt-Niederrad', 'Fredersdorf(b Berlin)', 'Freiberg(Neckar)', 'Freiberg(Sachs)', 'Freiburg(Breisgau) Hbf', 'Friedberg(Augsburg)', 'Friedberg(Hess)', 'Friedrich Wilhelmshütte', 'Friedrichsdorf(Taunus)', 'Friedrichsfeld(Niederrhein)', 'Furth(b Deisenhofen)', 'Fürstenberg(Havel)', 'Fürstenwalde(Spree)', 'Fürth(Bay)Hbf', 'Geislingen(Steige)', 'Gemünden(Main)', 'Giengen(Brenz)', 'Glauchau(Sachs)', 'Goldberg(Württ)', 'Gronau(Westf)', 'Groß-Rohrheim', 'Groß-Umstadt Wiebelsbach', 'Großauheim(Kr Hanau)', 'Großhesselohe Isartalbf', 'Grub(Oberbay)', 'Grünberg(Oberhess)', 'Gummersbach-Dieringhausen', 'Gundelfingen(Breisgau)', 'Halle(Saale)Hbf', 'Hallstadt(b Bamberg)', 'Hamburg Airport', 'Hamburg Alte Wöhr', 'Hamburg Berliner Tor', 'Hamburg Billwerder-Moorfleet', 'Hamburg Diebsteich', 'Hamburg Elbbrücken', 'Hamburg Elbgaustraße', 'Hamburg Friedrichsberg', 'Hamburg Hasselbrook', 'Hamburg Hochkamp', 'Hamburg Hoheneichen', 'Hamburg Holstenstraße', 'Hamburg Jungfernstieg', 'Hamburg Klein Flottbek', 'Hamburg Kornweg(Klein Borstel)', 'Hamburg Königstraße', 'Hamburg Landungsbrücken', 'Hamburg Landwehr', 'Hamburg Mittlerer Landweg', 'Hamburg Neuwiedenthal', 'Hamburg Reeperbahn', 'Hamburg Rübenkamp', 'Hamburg Stadthausbrücke', 'Hamburg Wandsbeker Chaussee', 'Hamburg-Allermöhe', 'Hamburg-Bahrenfeld', 'Hamburg-Barmbek', 'Hamburg-Blankenese', 'Hamburg-Eidelstedt', 'Hamburg-Hammerbrook', 'Hamburg-Harburg Rathaus', 'Hamburg-Heimfeld', 'Hamburg-Langenfelde', 'Hamburg-Nettelnburg', 'Hamburg-Ohlsdorf', 'Hamburg-Othmarschen', 'Hamburg-Ottensen', 'Hamburg-Poppenbüttel', 'Hamburg-Rissen', 'Hamburg-Rothenburgsort', 'Hamburg-Stellingen', 'Hamburg-Sternschanze', 'Hamburg-Sülldorf', 'Hamburg-Tiefstack', 'Hamburg-Veddel', 'Hamburg-Wellingsbüttel', 'Hamburg-Wilhelmsburg', 'Hamm(Westf)Hbf', 'Hannover Anderten-Misburg', 'Hannover Bismarckstr.', 'Hannover Flughafen', 'Hannover Messe/Laatzen', 'Hannover-Ledeburg', 'Hannover-Vinnhorst', 'Haste', 'Hattersheim(Main)', 'Hattingen(Ruhr)', 'Haßloch(Pfalz)', 'Heide(Holst)', 'Heidelberg Orthopädie', 'Heidelberg-Schlierbach/Ziegelhausen', 'Heidelberg-Weststadt/Südstadt', 'Heidesheim(Rheinhess)', 'Heimersheim/Lohrsdorf', 'Hennef im Siegbogen', 'Hennef(Sieg)', 'Hennigsdorf(b Berlin)', 'Heppenheim(Bergstr)', 'Herbolzheim(Breisg)', 'Herborn(Dillkr)', 'Hersbruck(r Pegnitz)', 'Herten(Westf)', 'Herzberg(Harz)', 'Hirschhorn(Neckar)', 'Hochheim(Main)', 'Hofheim(Taunus)', 'Hohen Neuendorf(b Berlin)', 'Homburg(Saar)Hbf', 'Hoppegarten(Mark)', 'Hornberg(Schwarzw)', 'Idstein(Taunus)', 'Illingen(Württ)', 'Immenhausen', 'Kahl(Main)', 'Kahla(Thür)', 'Karlstadt(Main)', 'Kempten(Allgäu)Hbf', 'Kirchhain(Bz Kassel)', 'Kirchheim(Neckar)', 'Kirchheim(Teck)', 'Kirchheim(Teck)-Ötlingen', 'Kronberg(Taunus)', 'Köln Geldernstr./Parkgürtel', 'Königstein(Sächs Schw)', 'Lage(Lippe)', 'Lahr(Schwarzw)', 'Lambrecht(Pfalz)', 'Landau(Isar)', 'Landau(Pfalz)Hbf', 'Landshut(Bay)Hbf', 'Langebrück(Sachs)', 'Langen(Hess)', 'Langenau(Württ)', 'Langenfeld(Rhld)', 'Langenfeld(Rhld)-Berghausen', 'Langenhagen Mitte', 'Langenhagen-Kaltenweide', 'Langenhorn(Schlesw)', 'Langweid(Lech)', 'Laudenbach(Bergstr)', 'Lauf(links Pegnitz)', 'Lauf(rechts Pegnitz)', 'Lauffen(Neckar)', 'Leer(Ostfriesl)', 'Leipzig/Halle Flughafen', 'Lengerich(Westf)', 'Leutesdorf(Rhein)', 'Lich(Oberhess)', 'Limburg(Lahn)', 'Lingen(Ems)', 'Linz(Rhein)', 'Lorch(Württ)', 'Ludwigshafen(Rh)Hbf', 'Ludwigshafen(Rhein) Mitte', 'Luisenthal(Saar)', 'Löbau(Sachs)', 'Löhne(Westf)', 'Löwenberg(Mark)', 'Lübben(Spreewald)', 'Lübbenau(Spreewald)', 'Lünen-Preußen', 'Mannheim ARENA/Maimarkt', 'Marbach(Neckar)', 'Marburg(Lahn)', 'Markdorf(Baden)', 'Meckenheim(Bz Köln)', 'Menden(Rheinl)', 'Merzig(Saar)', 'Metzingen(Württ)', 'Minden(Westf)', 'Morsum', 'Mosbach(Baden)', 'Mühlhausen(Thür)', 'Mühlheim(Main)', 'Mühlheim(Main)-Dietesheim', 'Mülheim(Ruhr)Hbf', 'Mülheim(Ruhr)Styrum', 'Mülheim(Ruhr)West', 'München Flughafen Besucherpark', 'München Flughafen Terminal', 'München Hackerbrücke', 'München Hirschgarten', 'München Leienfelsstr.', 'München St.Martin-Str.', 'München-Laim', 'München-Riem', 'Münster(W)Zentrum Nord', 'Münster(Westf)Hbf', 'Naumburg(Saale)Hbf', 'Neu-Isenburg', 'Neubrücke(Nahe)', 'Neuburg(Donau)', 'Neufahrn(Niederbay)', 'Neufahrn(b Freising)', 'Neuhaus(Pegnitz)', 'Neuhof(Kr Fulda)', 'Neukirchen(b Sulzb)', 'Neumarkt(Oberpf)', 'Neunkirchen(Saar)-Wellesweiler', 'Neunkirchen(Saar)Hbf', 'Neustadt am Rübenberge', 'Neustadt(Aisch)Bahnhof', 'Neustadt(Kr Marburg)', 'Neustadt(Schwarzw)', 'Neustadt(Weinstr)Hbf', 'Neuwirtshaus(Porscheplatz)', 'Niedernhausen(Taunus)', 'Nienburg(Weser)', 'Northeim(Han)', 'Nürnberg Frankenstadion', 'Nürnberg Ostring', 'Nürnberg Rothenburger Str.', 'Oberndorf(Neckar)', 'Obertshausen(Kr Of)', 'Oberursel(Taunus)', 'Offenbach(Main) Kaiserlei', 'Offenbach(Main) Ledermuseum', 'Offenbach(Main) Marktplatz', 'Offenbach(Main)Hbf', 'Offenbach(Main)Ost', 'Oldenburg(Oldb)Hbf', 'Osterhofen(Nby)', 'Ostheim(b Butzbach)', 'Ottersberg(Han)', 'Ottweiler(Saar)', 'Papenburg(Ems)', 'Petershausen(Obb)', 'Pfaffenhofen(Ilm)', 'Philippsburg(Baden)', 'Planegg', 'Plaue(Thür)', 'Plauen(Vogtl) ob Bf', 'Porz(Rhein)', 'Potsdam-Babelsberg', 'Pulling(b Freising)', 'Radldorf(Niederbay)', 'Reichenbach(Fils)', 'Reichenbach(Vogtl) ob Bf', 'Reinfeld(Holst)', 'Rheinfelden(Baden)', 'Rodenbach(b Hanau)', 'Rohrbach(Ilm)', 'Rohrbach(Saar)', 'Ronnenberg', 'Rosbach(Sieg)', 'Rostock-Evershagen', 'Rostock-Lichtenhagen', 'Rostock-Lütten Klein', 'Rotenburg(Wümme)', 'Rottenburg(Neckar)', 'Roßlau(Elbe)', 'Rudolstadt(Thür)', 'Röthenbach(Pegnitz)', 'Rückersdorf(Mfr)', 'Rüdesheim(Rhein)', 'Saalfeld(Saale)', 'Saarburg(Bz Trier)', 'Sandersleben(Anh)', 'Scheidt(Saar)', 'Schladern(Sieg)', 'Schwalbach(Taunus)Limes', 'Schwarzenfeld(Opf)', 'Schweich(DB)', 'Schwerte(Ruhr)', 'Schönebeck(Elbe)', 'Schönefeld(bei Berlin)', 'Sechtem', 'Seelze', 'Singen(Hohentwiel)', 'Sinsheim(Elsenz) Hbf', 'Sinzig(Rhein)', 'Soltau(Han)', 'Sonneberg(Thür)Hbf', 'St Georgen(Schwarzw)', 'St Goar', 'St Ilgen-Sandhausen', 'St Ingbert', 'St Michaelisdonn', 'St Wendel', 'Stadt Wehlen(Sachs)', 'Starnberg Nord', 'Steinach(bei Rothenburg ob der Tauber)', 'Steinau(Straße)', 'Steinbach am Wald', 'Steinheim(Main)', 'Stolberg(Rheinl)Hbf', 'Stuttgart Nürnberger Str.', 'Stuttgart Schwabstr.', 'Stuttgart-Untertürkheim', 'Stuttgart-Österfeld', 'Sulz(Neckar)', 'Sulzbach(Murr)', 'Sulzbach(Saar)', 'Tamm(Württ)', 'Taucha(Leipzig)', 'Tiengen(Hochrhein)', 'Türkheim(Bay)Bf', 'Uffing a Staffelsee', 'Urbach(b Schorndorf)', 'Vaihingen(Enz)', 'Varel(Oldb)', 'Velten(Mark)', 'Verden(Aller)', 'Villingen(Schwarzw)', 'Vilshofen(Niederbay)', 'Voerde(Niederrhein)', 'Völksen/Eldagsen', 'Wabern(Bz Kassel)', 'Walldorf(Hess)', 'Wangen(Allgäu)', 'Warburg(Westf)', 'Waren(Müritz)', 'Wedel(Holst)', 'Weiden(Oberpf)', 'Weiler(Rems)', 'Weilheim(Oberbay)', 'Weilimdorf', 'Weinheim(Bergstr)Hbf', 'Weißenburg(Bay)', 'Weißwasser(Oberlausitz)', 'Wendlingen(Neckar)', 'Wennigsen(Deister)', 'Werder(Havel)', 'Wernau(Neckar)', 'Westerland(Sylt)', 'Westheim(Schwab)', 'Wetter(Ruhr)', 'Weßling(Oberbay)', 'Wickede(Ruhr)', 'Wiesau(Oberpf)', 'Winden(Pfalz)', 'Winsen(Luhe)', 'Winterbach(b Schorndorf)', 'Wissen(Sieg)', 'Wolfen(Bitterfeld)', 'Wuppertal-Zoologischer Garten', 'Wörth(Isar)', 'Wörth(Rhein)', 'Wünsdorf-Waldstadt', 'Zepernick(Bernau)', 'Zwickau(Sachs)Hbf', 'Zwingenberg(Bergstr)']
        
        print(len(tt_names))
        if False:
            self.tt_cursor.execute(
                '''
                select station_name from stations
                ;''')
            names = [n[0] for n in self.tt_cursor.fetchall()]
            nn = []
            for n in names:
                try:
                    self.st_cursor.execute(
                        '''
                        select name from stations
                        where name = '{n}'
                        ;'''.format(n=n))
                    self.st_cursor.fetchall()[0]
                except:
                    # print(n, "not found")
                    nn.append(n)
            nn.sort()
            print(nn)

            tt_names = nn

        st_names = ['Ahlen (Westf)', 'Ahlten (Han)', 'Albrechtshof', 'Alfeld (Leine)', 'Allermöhe', 'Alsfeld (Oberhess)', 'Alte Wöhr (Stadtpark)', 'Altena (Westf)', 'Anderten-Misburg', 'Arnsberg (Westf)', 'Arnsdorf (b Dresden)', 'Ascheberg (Holst)', 'Au (Sieg)', 'Aßling (Oberbay)', 'Babelsberg', 'Babenhausen (Hess)', 'Bad Honnef (Rhein)', 'Bad Münder (Deister)', 'Bad Münster am Stein', 'Bad Neustadt (Saale)', 'Bad Soden (Taunus)', 'Baden (Kr Verden)', 'Bahrenfeld', 'Balingen (Württ)', 'Barmbek', 'Barnstorf (Han)', 'Benningen (Neckar)', 'Bergfelde (b Berlin)', 'Berlin Alt Reinickendorf', 'Berlin Anhalter Bahnhof', 'Berlin Attilastraße', 'Berlin Bornholmer Straße', 'Berlin Feuerbachstraße', 'Berlin Greifswalder Straße', 'Berlin Hauptbahnhof', 'Berlin Messe Nord/ZOB', 'Berlin Pichelsberg', 'Berlin Poelchaustraße', 'Berlin Raoul-Wallenberg-Straße', 'Berlin Storkower Straße', 'Berlin Sundgauer Straße', 'Berlin Wuhlheide', 'Berlin Yorckstraße', 'Berlin Yorckstraße/Großgörschenstraße', 'Berlin-Baumschulenweg', 'Berlin-Karlshorst', 'Berlin-Rummelsburg Betriebsbahnhof', 'Berlin-Tegel', 'Berlin-Wedding', 'Berlin-Westend', 'Berliner Tor', 'Bernau (b Berlin)', 'Bernau a. Chiemsee', 'Betzdorf (Sieg)', 'Biberach (Baden)', 'Biberach (Riß)', 'Bickenbach (Bergstr)', 'Bietigheim (Baden)', 'Billwerder-Moorfleet', 'Bingen (Rhein) Hbf', 'Bingen (Rhein) Stadt', 'Birkenwerder (b Berlin)', 'Blankenburg (Harz)', 'Blankenese', 'Blankenfelde (Kr Teltow-Fläming)', 'Bondorf (b Herrenberg)', 'Bonn-Bad Godesberg', 'Borken (Hess)', 'Borna (b Leipzig)', 'Bornheim-Sechtem', 'Borsdorf (Sachs)', 'Brake (b Bielefeld)', 'Brühl', 'Brühl-Kierberg', 'Buchenau (Oberbay)', 'Buchholz (Nordheide)', 'Bullay (DB)', 'Burg (b Magdeburg)', 'Burgau (Schwab)', 'Burgdorf (Han)', 'Böbingen (Rems)', 'Büchen', 'Bühl (Baden)', 'Bünde (Westf)', 'Bürstadt (Ried)', 'Calau (Niederlausitz)', 'Calbe (Saale) Ost', 'Celle Pbf', 'Cham (Oberpf)', 'Cochem (Mosel)', 'Coesfeld (Westf)', 'Coswig (b Dresden)', 'Creußen (Oberfr)', 'Dedensen / Gümmer', 'Dettingen (Main)', 'Diebsteich', 'Diedorf (Schwab)', 'Dieringhausen', 'Dietzenbach-Mitte', 'Dillingen (Donau)', 'Dillingen (Saar)', 'Duisburg Schlenk', 'Düsseldorf Völklinger Straße', 'Düsseldorf Zoo', 'Düsseldorf-Friedrichstadt', 'Ebenhausen (Unterfr)', 'Ebersbach (Fils)', 'Ebersbach (Sachs)', 'Ebersberg (Oberbay)', 'Egestorf (Deister)', 'Ehingen (Donau)', 'Ehningen (b Böblingen)', 'Ehrang', 'Eichenau (Oberbay)', 'Eidelstedt', 'Eilsleben (b Magdeburg)', 'Eislingen (Fils)', 'Elbbrücken', 'Elbgaustraße', 'Ellingen (Bay)', 'Elze (Han)', 'Ennepetal (Gevelsberg)', 'Erbach (Württ)', 'Erzingen (Baden)', 'Esslingen (Neckar)', 'Eutingen (Baden)', 'Falkenberg (Elster)', 'Falkensee', 'Feldkirchen (b München)', 'Finsterwalde (Niederlausitz)', 'Fischbach (b Nürnberg)', 'Flughafen Leipzig/Halle', 'Flughafen München', 'Flughafen München Besucherpark', 'Flörsheim (Main)', 'Forchheim (Oberfr)', 'Forchheim (b Karlsruhe)', 'Frankfurt (Main) Flughafen Regionalbahnhof', 'Frankfurt (Main) Galluswarte', 'Frankfurt (Main) Ginnheim', 'Frankfurt (Main) Hauptwache', 'Frankfurt (Main) Hbf', 'Frankfurt (Main) Konstablerwache', 'Frankfurt (Main) Lokalbahnhof', 'Frankfurt (Main) Mühlberg', 'Frankfurt (Main) Niederrad', 'Frankfurt (Main) Ost', 'Frankfurt (Main) Ostendstraße', 'Frankfurt (Main) Stadion', 'Frankfurt (Main) Stresemannallee', 'Frankfurt (Main) Süd', 'Frankfurt (Main) Taunusanlage', 'Frankfurt (Main) West', 'Frankfurt (Oder)', 'Frankfurt am Main Flughafen Fernbahnhof', 'Frankfurt am Main Gateway Gardens', 'Frankfurt am Main Messe', 'Frankfurt-Höchst Farbwerke', 'Fredersdorf (b Berlin)', 'Freiberg (Neckar)', 'Freiberg (Sachs)', 'Freiburg (Breisgau) Hbf', 'Friedberg (Hess)', 'Friedberg (b Augsburg)', 'Friedrich-Wilhelms-Hütte', 'Friedrichsberg', 'Friedrichsdorf (Taunus)', 'Friedrichsfeld (Niederrhein)', 'Furth (b Deisenhofen)', 'Fürstenberg (Havel)', 'Fürstenwalde (Spree)', 'Fürth (Bay) Hbf', 'Geislingen (Steige)', 'Gemünden (Main)', 'Giengen (Brenz)', 'Glauchau (Sachs)', 'Goldberg', 'Gronau (Westf)', 'Groß Rohrheim', 'Groß Umstadt-Wiebelsbach', 'Großauheim (Kr Hanau)', 'Großhesselohe Isartalbahnhof', 'Grub (Oberbay)', 'Grünberg (Oberhess)', 'Gundelfingen', 'HD-Weststadt/Südstadt', 'Halle (Saale) Hbf', 'Hallstadt (b Bamberg)', 'Hamburg Airport (Flughafen)', 'Hamburg-Wandsbek', 'Hamm (Westf) Hbf', 'Hammerbrook', 'Hannover - Ledeburg', 'Hannover - Vinnhorst', 'Hannover Bismarckstraße', 'Hannover-Flughafen', 'Hannover-Messe / Laatzen', 'Harburg Rathaus', 'Hasselbrook', 'Haste (Han)', 'Hattersheim (Main)', 'Hattingen (Ruhr)', 'Haßloch (Pfalz)', 'Heide (Holst)', 'Heidelberg-Orthopädie', 'Heidelberg-Schlierbach-Ziegelhausen', 'Heidesheim (Rheinhess)', 'Heimersheim / Lohrsdorf', 'Heimfeld', 'Hennef (Sieg)', 'Hennef Im Siegbogen', 'Hennigsdorf (b Berlin)', 'Heppenheim (Bergstr)', 'Herbolzheim (Breisgau)', 'Herborn (Dillkr)', 'Hersbruck (rechts Pegnitz)', 'Herten (Westf)', 'Herzberg (Harz)', 'Hirschhorn (Neckar)', 'Hochheim (Main)', 'Hochkamp', 'Hofheim (Taunus)', 'Hohen Neuendorf (b Berlin)', 'Hoheneichen', 'Holstenstraße', 'Homburg (Saar) Hbf', 'Hoppegarten (Mark)', 'Hornberg', 'Idstein (Taunus)', 'Illingen (Württ)', 'Immenhausen (Hess)', 'Jungfernstieg', 'Kahl (Main)', 'Kahla (Thür)', 'Karlstadt (Main)', 'Kempten (Allgäu) Hbf', 'Kirchhain (Bz Kassel)', 'Kirchheim (Neckar)', 'Kirchheim (Teck)', 'Kirchheim (Teck)-Ötlingen', 'Klein Flottbek', 'Kohlscheid', 'Kornweg (Klein Borstel)', 'Kronberg (Taunus)', 'Kurort Altenberg (Erzgeb)', 'Köln-Geldernstr./Parkgürtel', 'Königstein (Sächs Schweiz)', 'Königstraße', 'Lage (Lippe)', 'Lahr (Schwarzw)', 'Lambrecht (Pfalz)', 'Landau (Isar)', 'Landau (Pfalz) Hbf', 'Landshut (Bay) Hbf', 'Landungsbrücken', 'Landwehr', 'Langebrück (Sachs)', 'Langen (Hess)', 'Langenau (Württ)', 'Langenfeld (Rheinl)', 'Langenfeld (Rheinl)-Berghausen', 'Langenfelde', 'Langenhagen - Kaltenweide', 'Langenhagen-Mitte', 'Langenhorn (Schlesw)', 'Langweid (Lech)', 'Laudenbach (Bergstr)', 'Lauf (links Pegnitz)', 'Lauf (rechts Pegnitz)', 'Lauffen (Neckar)', 'Leer (Ostfriesl)', 'Lengerich (Westf)', 'Leutesdorf (Rhein)', 'Lich (Oberhess)', 'Limburg (Lahn)', 'Lingen (Ems)', 'Linz (Rhein)', 'Lorch (Württ)', 'Ludwigshafen (Rhein) Hbf', 'Ludwigshafen (Rhein) Mitte', 'Ludwigslust', 'Luisenthal (Saar)', 'Löbau (Sachs)', 'Löhne (Westf)', 'Löwenberg (Mark)', 'Lübben (Spreewald)', 'Lübbenau (Spreewald)', 'Lünen Preußen', 'Malmsheim', 'Mannheim ARENA / Maimarkt', 'Marbach (Neckar)', 'Marburg (Lahn)', 'Markdorf (Baden)', 'Meckenheim', 'Menden (Rheinl)', 'Merzig (Saar)', 'Metzingen (Württ)', 'Minden (Westf)', 'Mittlerer Landweg', 'Morsum (Sylt)', 'Mosbach (Baden)', 'Mühlhausen (Thür)', 'Mühlheim (Main)', 'Mühlheim-Dietesheim', 'Mülheim (Ruhr) Hbf', 'Mülheim (Ruhr) West', 'Mülheim (Ruhr)-Styrum', 'München Leienfelsstraße', 'München St Martin Straße', 'München-Hackerbrücke', 'München-Hirschgarten', 'München-Laim Pbf', 'München-Riem Pbf', 'Münster (Westf) Hbf', 'Münster Zentrum Nord', 'Nauen', 'Naumburg (Saale) Hbf', 'Nettelnburg', 'Neu Isenburg', 'Neubrücke (Nahe)', 'Neuburg (Donau)', 'Neufahrn (Niederbay)', 'Neufahrn (b Freising)', 'Neuhaus (Pegnitz)', 'Neuhof (Kr Fulda)', 'Neukirchen (b Sulzb)', 'Neumarkt (Oberpf)', 'Neunkirchen (Saar) Hbf', 'Neunkirchen (Saar)-Wellesweiler', 'Neustadt (Aisch) Bahnhof', 'Neustadt (Dosse)', 'Neustadt (Kr Marburg)', 'Neustadt (Schwarzw)', 'Neustadt (Weinstr) Hbf', 'Neustadt a Rübenberge', 'Neuwiedenthal', 'Neuwirtshaus (Porscheplatz)', 'Niedernhausen (Taunus)', 'Nienburg (Weser)', 'Northeim (Han)', 'Nürnberg Rothenburger Straße', 'Nürnberg-Frankenstadion', 'Nürnberg-Ostring', 'Oberndorf (Neckar)', 'Obertshausen (Kr Offenbach)', 'Oberursel (Taunus)', 'Oberwinter', 'Offenbach (Main) Hbf', 'Offenbach (Main) Kaiserlei', 'Offenbach (Main) Ledermuseum', 'Offenbach (Main) Marktplatz', 'Offenbach (Main) Ost', 'Ohlsdorf', 'Oldenburg (Oldb) Hbf', 'Osterhofen (Niederbay)', 'Ostheim (b Butzbach)', 'Othmarschen', 'Ottensen', 'Ottersberg (Han)', 'Ottweiler (Saar)', 'Papenburg (Ems)', 'Petershausen (Oberbay)', 'Pfaffenhofen (Ilm)', 'Philippsburg (Baden)', 'Planegg (Krailling)', 'Plaue (Thür)', 'Plauen (Vogtl) ob Bf', 'Poppenbüttel', 'Porz (Rhein)', 'Pulling (b Freising)', 'Radldorf (Niederbay)', 'Reeperbahn', 'Reichenbach (Fils)', 'Reichenbach (Vogtl) ob Bf', 'Reinfeld (Holst)', 'Rheinfelden (Baden)', 'Rissen', 'Rodenbach bei Hanau', 'Rohrbach (Ilm)', 'Rohrbach (Saar)', 'Ronnenberg (Han)', 'Rosbach (Sieg)', 'Rostock Evershagen', 'Rostock Lichtenhagen', 'Rostock Lütten Klein', 'Rotenburg (Wümme)', 'Rothenburgsort', 'Rottenburg (Neckar)', 'Roßlau (Elbe)', 'Rudolstadt (Thür)', 'Röthenbach (Pegnitz)', 'Rübenkamp', 'Rückersdorf (Mittelfr)', 'Rüdesheim (Rhein)', 'Saalfeld (Saale)', 'Saarburg (Bz Trier)', 'Sandersleben (Anh)', 'Scheidt (Saar)', 'Schladern (Sieg)', 'Schwalbach (Taunus) Limes', 'Schwarzenbek', 'Schwarzenfeld (Oberpf)', 'Schweich (DB)', 'Schwerte (Ruhr)', 'Schönebeck (Elbe)', 'Schönefeld (bei Berlin)', 'Seegefeld', 'Seelze Pbf', 'Singen (Hohentwiel)', 'Sinsheim (Elsenz) Hbf', 'Sinzig (Rhein)', 'Soltau (Han)', 'Sonneberg (Thür) Hbf', 'St. Georgen (Schwarzw)', 'St. Goar', 'St. Ilgen/Sandhausen', 'St. Ingbert', 'St. Michaelisdonn', 'St. Wendel', 'Stadt Wehlen (Sachs)', 'Stadthausbrücke', 'Starnberg-Nord', 'Steinach (b Rothenburg o.d. Tauber)', 'Steinau (Straße)', 'Steinbach a Wald', 'Steinheim am Main (Hanau)', 'Stellingen', 'Sternschanze', 'Stolberg (Rheinl) Hbf', 'Stuttgart Nürnberger Straße', 'Stuttgart Schwabstraße', 'Stuttgart Österfeld', 'Stuttgart-Untertürkheim Pbf', 'Stuttgart-Weilimdorf', 'Sulz (Neckar)', 'Sulzbach (Murr)', 'Sulzbach (Saar)', 'Sülldorf', 'Tamm (Württ)', 'Taucha (b Leipzig)', 'Tiefstack', 'Tiengen (Hochrhein)', 'Türkheim (Bay)', 'Uffing am Staffelsee', 'Urbach (b Schorndorf)', 'Vaihingen (Enz)', 'Varel (Oldb)', 'Veddel', 'Velten (Mark)', 'Verden (Aller)', 'Villingen (Schwarzw)', 'Vilshofen (Niederbay)', 'Voerde (Niederrhein)', 'Völksen-Eldagsen', 'Wabern (Bz Kassel)', 'Walldorf (Hess)', 'Wandsbeker Chaussee', 'Wangen (Allgäu)', 'Warburg (Westf)', 'Waren (Müritz)', 'Wedel (Holst)', 'Weiden (Oberpf)', 'Weil der Stadt', 'Weiler (Rems)', 'Weilheim (Oberbay)', 'Weinheim (Bergstr) Hbf', 'Weißenburg (Bay)', 'Weißwasser (Oberlausitz)', 'Wellingsbüttel', 'Wendlingen (Neckar)', 'Wennigsen (Deister)', 'Werder (Havel)', 'Wernau (Neckar)', 'Westerland (Sylt)', 'Westheim (Schwab)', 'Wetter (Ruhr)', 'Weßling (Oberbay)', 'Wickede (Ruhr)', 'Wiesau (Oberpf)', 'Wilhelmsburg', 'Winden (Pfalz)', 'Winsen (Luhe)', 'Winterbach (b Schorndorf)', 'Wissen (Sieg)', 'Wittenberge', 'Wolfen (Bitterfeld)', 'Wuppertal Zoologischer Garten', 'Wörth (Isar)', 'Wörth (Rhein)', 'Wünsdorf Waldstadt', 'Zepernick (b Bernau)', 'Zwickau (Sachs) Hbf', 'Zwingenberg (Bergstr)']
        print(len(st_names))
        if False:
            self.st_cursor.execute(
                '''select name 
                from stations
                where category <= 5;''')
            names = [n[0] for n in self.st_cursor.fetchall()]
            nn = []
            for n in names:
                try:
                    self.tt_cursor.execute(
                        '''
                        select station_name from stations
                        where station_name = '{n}'
                        ;'''.format(n=n))
                    self.tt_cursor.fetchall()[0]
                except:
                    # print(n, "not found")
                    nn.append(n)
            nn.sort()
            print(nn)
        
        st_no_match = []

        i = 0
        subt = {}
        while i < len(st_names):
            n = st_names[i]
            found = False
            for j in range(len(tt_names)):
                m = tt_names[j]
                try:
                    if translator[m] == n:
                        st_names.remove(n)
                        tt_names.remove(m)
                        found = True
                        break
                except:
                    pass
                if (n.replace(" ","") == m or 
                        n.replace("Main","M").replace(" ","") == m or 
                        n.replace(" (Main) ","-") == m or 
                        n.replace(" am Main ","(Main)").replace(" ","") == m or 
                        n.replace(" ","-") == m or
                        n.replace("-"," ") == m or
                        n.replace(".","") == m or
                        n.replace("traße","tr.") == m or
                        n.replace("traße","tr") == m or
                        n.replace("Hauptbahnhof","Hbf") == m or
                        n.replace(" Pbf","") == m or
                        "Hamburg " + n == m or
                        "Hamburg-" + n == m or
                        n.replace(" (","(") == m or
                        n.replace(" (b ","(") == m
                        ):
                    st_names.remove(n)
                    tt_names.remove(m)
                    subt[m] = n
                    found = True
                    break
            if not found:
                i += 1
        print("st", st_names, len(st_names))
        print("tt", tt_names, len(tt_names))
        print(subt)

        # finally we're left with 23 unmatched stations from the station_data API response:
        st = ['Albrechtshof', 'Berlin-Karlshorst', 'Berlin-Wedding', 'Bonn-Bad Godesberg', 'Brühl', 'Brühl-Kierberg', 'Büchen', 'Bürstadt (Ried)', 'Ehrang', 'Falkensee', 'Frankfurt-Höchst Farbwerke', 'Hamburg-Wandsbek', 'Kohlscheid', 'Kurort Altenberg (Erzgeb)', 'Ludwigslust', 'Malmsheim', 'Nauen', 'Neustadt (Dosse)', 'Oberwinter', 'Schwarzenbek', 'Seegefeld', 'Weil der Stadt', 'Wittenberge']


    def insert_translated_names(self):
        # for (key, value) in translator.items():
        #     self.tt_cursor.execute(
        #         '''
        #         update stations set stada_name = '{st_name}' 
        #         where station_name = '{tt_name}'
        #         ;'''.format(st_name = value, tt_name = key)
        #     )
        #     # data = self.tt_cursor.fetchall()
        #     # print(data)
        #     self.tt_client.commit()
        self.tt_cursor.execute(
            '''
            update stations set stada_name = station_name
            where stada_name is null;
            '''
        )
        self.tt_client.commit()
        
if __name__ == "__main__":
    pgq = pg_query_handler()
    # pgq.get_non_matching_names()
    pgq.insert_translated_names()