xml_doc = """
<WalkTowardsPos>
    <InputPort local="pos" bb="walk_goal" />
    <InputPort local="action_status" bb="action_status" />
    <OutputPort local="action_status" bb="action_status" />
</WalkTowardsPos>
"""


from bs4 import BeautifulSoup
soup = BeautifulSoup(xml_doc, 'xml')

# print(soup.prettify())
walker=soup.find("WalkTowardsPos")
inputs=walker.find_all("InputPort")

pos=walker.find(local="pos")

pos=walker.find("InputPort",local="action_status")
print(pos or "default")

# <html>
#  <head>
#   <title>
#    The Dormouse's story
#   </title>
#  </head>
#  <body>
#   <p class="title">
#    <b>
#     The Dormouse's story
#    </b>
#   </p>
#   <p class="story">
#    Once upon a time there were three little sisters; and their names were
#    <a class="sister" href="http://example.com/elsie" id="link1">
#     Elsie
#    </a>
#    ,
#    <a class="sister" href="http://example.com/lacie" id="link2">
#     Lacie
#    </a>
#    and
#    <a class="sister" href="http://example.com/tillie" id="link2">
#     Tillie
#    </a>
#    ; and they lived at the bottom of a well.
#   </p>
#   <p class="story">
#    ...
#   </p>
#  </body>
# </html>