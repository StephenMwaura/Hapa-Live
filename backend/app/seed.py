from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Event

SAMPLE_EVENTS = [
    {"slug":"keinemusik-nairobi-2026","title":"Keinemusik Nairobi","artist":"&ME · Rampa · Adam Port","city":"Nairobi","venue":"Uhuru Gardens Memorial Park","starts_at":datetime(2026,11,21,16,0),"price_from_kes":6500,"genre":"Electronic","source_url":"https://www.quicket.co.ke/events/390611-keinemusik-nairobi/","source_label":"Quicket","art":"keinemusik","featured":True},
    {"slug":"tuff-lion-album-launch-2026","title":"Tuff Lion Album Launch","artist":"The Remake Movement","city":"Nairobi","venue":"Nairobi Street Kitchen, Westlands","starts_at":datetime(2026,11,7,18,0),"price_from_kes":1500,"genre":"Reggae","source_url":"https://nairobicity.co.ke/events/162","source_label":"NairobiCity","art":"tuff-lion","featured":False},
    {"slug":"sauti-kulture-2026","title":"Sauti Kulture","artist":"Fari Athman · Doroh · Kendy · more","city":"Nairobi","venue":"Vibanda Village, Upper Hill","starts_at":datetime(2026,11,28,18,0),"price_from_kes":1000,"genre":"Afro fusion","source_url":"https://zivoratickethub.com/events/sauti-kulture","source_label":"Zivora","art":"afro","featured":False},
    {"slug":"friday-jazz-night-2026-11-06","title":"Friday Jazz Night","artist":"Live jazz · dinner & drinks","city":"Nairobi","venue":"Artisan Deli, Karen","starts_at":datetime(2026,11,6,17,0),"price_from_kes":None,"genre":"Jazz","source_url":"https://kenyabuzz.com/events/","source_label":"KenyaBuzz","art":"jazz","featured":False},
    {"slug":"bar-symphony-2026-11-07","title":"The Bar Symphony","artist":"Live band experience","city":"Nairobi","venue":"Alloy Bar and Lounge","starts_at":datetime(2026,11,7,17,0),"price_from_kes":2000,"genre":"Live band","source_url":"https://woza.tickets/calendar","source_label":"WOZA","art":"festival","featured":False},
    {"slug":"kimani-friends-2026-11-07","title":"Kimani & Friends","artist":"A live music session","city":"Nairobi","venue":"Ayira's Neuro-Soul Cafe","starts_at":datetime(2026,11,7,17,0),"price_from_kes":1200,"genre":"Live band","source_url":"https://woza.tickets/calendar","source_label":"WOZA","art":"gospel","featured":False},
    {"slug":"sawa-at-the-beach-diani-2026","title":"SAWA – At the Beach","artist":"Joey Alaniz · Dora · L3mayian · more","city":"Diani","venue":"The 41 Beach Club","starts_at":datetime(2026,12,31,19,0),"price_from_kes":3000,"genre":"Electronic","source_url":"https://www.sawalounge.com/","source_label":"SAWA","art":"sawa","featured":False},
    {"slug":"kisumu-olskool-rnb-brunch-2026","title":"Kisumu Ol’Skool RNB Brunch in the Wild","artist":"Old-school RNB experience","city":"Kisumu","venue":"Impala Animal Park","starts_at":datetime(2026,12,5,12,0),"price_from_kes":1499,"genre":"R&B","source_url":"https://ticketyetu.com/events/kisumu-ol-skool-rnb-brunch-in-the-wild--CibRg","source_label":"Ticketyetu","art":"kisumu-rnb","featured":False},
    {"slug":"east-africa-dancehall-mombasa-2026","title":"East Africa Dancehall Concert – 2nd Anniversary","artist":"Dancehall · East African artists","city":"Mombasa","venue":"Butterfly Pavilion","starts_at":datetime(2026,12,26,18,0),"price_from_kes":700,"genre":"Dancehall","source_url":"https://soldoutafrica.com/east-africa-dancehall-concert-2nd-anniversary","source_label":"SoldOutAfrica","art":"dancehall-mombasa","featured":False},
    {"slug":"solfest-2026-fan-show","title":"Sol Fest 2026 – Fan Show","artist":"Fan Show lineup to be announced","city":"Nairobi","venue":"Nairobi · venue to be confirmed","starts_at":datetime(2026,12,19,16,0),"price_from_kes":3526,"genre":"Afro-pop","source_url":"https://solfest.hustlesasa.shop/products/694d22411f68b6012b2f8005","source_label":"Solfest tickets","art":"solfest","featured":False},
    {"slug":"detty-dezemba-festival-2026","title":"Detty Dezemba Festival","artist":"Wizkid · Uncle Waffles · more","city":"Nairobi","venue":"Venue to be announced","starts_at":datetime(2026,12,12,14,0),"price_from_kes":3500,"genre":"Afrobeats · Amapiano","source_url":"https://weareafr0.co.ke/events/detty-dezemba","source_label":"WeWannaParty · Kolacopia","art":"detty","featured":False},
]


def seed_events(db: Session) -> None:
    for data in SAMPLE_EVENTS:
        event = db.scalar(select(Event).where(Event.slug == data["slug"]))
        if event is None:
            db.add(Event(**data))
        else:
            for field, value in data.items():
                setattr(event, field, value)
    db.commit()
