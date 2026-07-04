xml_doc = """
<WalkTowardsPos>
    <InputPort local="pos" bb="walk_goal" />
    <InputPort local="action_status" bb="action_status" />
    <OutputPort local="action_status" bb="action_status" />
</WalkTowardsPos>
"""


from bs4 import BeautifulSoup

soup = BeautifulSoup(xml_doc, "xml")

# print(soup.prettify())
walker = soup.find("WalkTowardsPos")
inputs = walker.find_all("InputPort")

pos = walker.find(local="pos")

pos = walker.find("InputPort", local="action_status")
print(pos or "default")


a = {}
print(a.keys())
for i in a.keys():
    print(i)
