<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.1" name="sprites_1_1" tilewidth="34" tileheight="49" spacing="1" tilecount="40" columns="10">
 <tileoffset x="-1" y="1"/>
 <image source="../art/sprites_1_1.png" trans="000000" width="349" height="199"/>
 <tile id="12">
  <properties>
   <property name="can_walk" type="bool" value="false"/>
   <property name="tree" value="5"/>
  </properties>
 </tile>
 <tile id="22">
  <properties>
   <property name="can_walk" type="bool" value="false"/>
   <property name="tree" value="5"/>
  </properties>
 </tile>
 <tile id="32">
  <properties>
   <property name="can_walk" type="bool" value="false"/>
   <property name="tree" value="5"/>
  </properties>
 </tile>
 <wangsets>
  <wangset name="trees" type="edge" tile="12">
   <wangcolor name="trees" color="#005500" tile="12" probability="1"/>
   <wangtile tileid="12" wangid="1,0,1,0,1,0,1,0"/>
   <wangtile tileid="22" wangid="1,0,1,0,1,0,1,0"/>
   <wangtile tileid="32" wangid="1,0,1,0,1,0,1,0"/>
  </wangset>
 </wangsets>
</tileset>
