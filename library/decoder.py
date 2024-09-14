import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Decode:
    photos: Optional[List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    amount: Optional[str] = None
    price: Optional[str] = None
    url: Optional[str] = None


def decode(data: str):
    data = data.splitlines()
    results = []

    for _id, line in enumerate(data):
        match = re.search(
            r"photos=\[(.*?)\], title='(.+?)', description='(.+?)', category='(.+?)', subcategory='(.+?)', sizes=\[(.*?)\], colors=\[(.*?)\], .*?amount=(\d+), .*?price=(\d+), url='(.+?)'",
            line)

        if match:
            photos = match.group(1).replace("'", "").split(", ")
            title = match.group(2)
            description = match.group(3).replace('||', '\n')
            category = match.group(4)
            subcategory = match.group(5)
            sizes = match.group(6).replace("'", "").split(", ")
            colors = match.group(7).replace("'", "").split(", ")
            amount = match.group(8)
            price = match.group(9)
            url = match.group(10)

            decoded_item = Decode(
                photos=photos,
                title=title,
                description=description,
                category=category,
                subcategory=subcategory,
                sizes=sizes,
                colors=colors,
                amount=amount,
                price=price,
                url=url
            )
            results.append(decoded_item)
        else:
            print(f"Невозможно распарсить строку: {_id+1}")

    return results
