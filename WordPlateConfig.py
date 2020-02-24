#!/usr/bin/python
# coding: utf-8

import os
import time
import random
import json
import ConfigParser
import wx



class BaseConfig:
    """configure"""
    
    def __init__(self):

        self.word_plate_player_count = 2
        self.word_plate_banker_seat_id = 0
        self.word_plate_test_count = 0
        self.word_plate_total_count = 0
        self.word_plate_everyone_count = 14
        self.heap_word_plate_datas = []
        self.player_word_plate_datas = []
        
    def Reset(self):
        
        self.word_plate_player_count = 2
        self.word_plate_banker_seat_id = 0
        self.word_plate_test_count = 0
        self.word_plate_total_count = 0
        self.word_plate_everyone_count = 14
        self.heap_word_plate_datas = []
        self.player_word_plate_datas = []
        

    def Read(self, path):
        
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(path,'r'))
        except:
            print(path, "read error!")
            return False
        
        self.Reset()

        if config.has_section("Options"):

            if config.has_option("Options", "player_count"):
                self.word_plate_player_count = config.getint("Options", "player_count")                 
                
            if config.has_option("Options", "banker_seat_id"):
                self.word_plate_banker_seat_id = config.getint("Options", "banker_seat_id")
            
            if config.has_option("Options", "test_count"):
                self.word_plate_test_count = config.getint("Options", "test_count")
            
            if config.has_option("Options", "total_count"):
                self.word_plate_total_count = config.getint("Options", "total_count")                
  
            if config.has_option("Options", "everyone_count"):
                self.word_plate_everyone_count = config.getint("Options", "everyone_count")             
        
        if config.has_section("WordPlateDatas"):
         
            if config.has_option("WordPlateDatas","heap_word_plate_datas"):
                word_plate_datas = config.get("WordPlateDatas", "heap_word_plate_datas")
                word_plate_datas = word_plate_datas.split(",")
                
                for word_plate_data in word_plate_datas:
                    if len(word_plate_data) > 0:
                        self.heap_word_plate_datas.append(int(word_plate_data, 16))
            
            if self.word_plate_player_count > 0:
                for seat_id in range(self.word_plate_player_count):
                    if config.has_option("WordPlateDatas", "player_word_plate_datas%d"%(seat_id)):
                        word_plate_datas = config.get("WordPlateDatas", "player_word_plate_datas%d"%(seat_id))
                        word_plate_datas = word_plate_datas.split(",")
                        
                        player_word_plate_datas = []
                        for word_plate_data in word_plate_datas:
                            if len(word_plate_data) > 0:
                                player_word_plate_datas.append(int(word_plate_data, 16))
                            
                        self.player_word_plate_datas.append(player_word_plate_datas)
                
            
        return True
    
    

    def Write(self, path):
        
        config = ConfigParser.ConfigParser()
        if not config.has_section("Options"):
            config.add_section("Options")

        if not config.has_section("WordPlateDatas"):
            config.add_section("WordPlateDatas")
            
        config.set("Options", "player_count", self.word_plate_player_count)
        config.set("Options", "banker_seat_id", self.word_plate_banker_seat_id)
        config.set("Options", "test_count", self.word_plate_test_count)
        config.set("Options", "total_count", self.word_plate_total_count)
        config.set("Options", "everyone_count", self.word_plate_everyone_count)         
        
        heap_word_plate_datas = []
        for word_plate_data in self.heap_word_plate_datas:
            heap_word_plate_datas.append("0x{:0>2X}".format(word_plate_data))
        heap_word_plate_datas = ",".join(heap_word_plate_datas)
        config.set("WordPlateDatas", "heap_word_plate_datas", heap_word_plate_datas)
        
        if self.word_plate_player_count > 0:
            for seat_id in range(self.word_plate_player_count):
                if seat_id < len(self.player_word_plate_datas):
                    one_player_word_plate_datas = self.player_word_plate_datas[seat_id]
                    if len(one_player_word_plate_datas) > 0:
                        word_plate_datas = []
                        for word_plate_data in one_player_word_plate_datas:
                            word_plate_datas.append("0x{:0>2X}".format(word_plate_data))
                        one_player_word_plate_datas = ",".join(word_plate_datas)
                        config.set("WordPlateDatas", "player_word_plate_datas%d"%(seat_id), one_player_word_plate_datas)

        try:
            config.write(open(path, 'w'))
        except:
            print("wirte error!")
            return False
        
        return True
    

class WordPlateConfig(BaseConfig):

    def __init__(self):
        
        BaseConfig.__init__(self)
        
    def ReadJson(self, path):
    
        try:
            fp = open(path, 'r')
        except:
            print(path, "open json file error!")
            return False
        
        self.Reset()
        
        config = {}
        with fp:
            try:
                check_bom = fp.read(3)
                if check_bom == '\xef\xbb\xbf':
                    fp.seek(3)
                else:
                    fp.seek(0)
                config = json.load(fp, "utf-8")
            except BaseException as err:
                print("json read error",err)
                return False, err
            
            
        if type(config) == type({}) and len(config) > 0:
            if config.has_key("Options"):
                
                if config["Options"].has_key("player_count"):
                    self.word_plate_player_count = config["Options"]["player_count"]
                
                if config["Options"].has_key("banker_seat_id"):
                    self.word_plate_banker_seat_id = config["Options"]["banker_seat_id"]
                    
                if config["Options"].has_key("test_count"):
                    self.word_plate_test_count = config["Options"]["test_count"]
                    
                if config["Options"].has_key("total_count"):
                    self.word_plate_total_count = config["Options"]["total_count"]
                    
                if config["Options"].has_key("everyone_count"):
                    self.word_plate_everyone_count = config["Options"]["everyone_count"]                        
                
            if config.has_key("WordPlateDatas"):
                
                if config["WordPlateDatas"].has_key("heap_word_plate_datas"):
                    word_plate_datas = config["WordPlateDatas"]["heap_word_plate_datas"]
                    word_plate_datas = word_plate_datas.split(",")
                    
                    for word_plate_data in word_plate_datas:
                        if len(word_plate_data) > 0:                       
                            self.heap_word_plate_datas.append(int(word_plate_data, 16))   
                        
                if config["WordPlateDatas"].has_key("player_word_plate_datas") and len(config["WordPlateDatas"]["player_word_plate_datas"]) > 0:
                    if self.word_plate_player_count > 0:
                        for seat_id in range(self.word_plate_player_count):
                            if seat_id < len(config["WordPlateDatas"]["player_word_plate_datas"]):     
                                word_plate_datas = config["WordPlateDatas"]["player_word_plate_datas"][seat_id]
                                word_plate_datas = word_plate_datas.split(",")
                            
                                player_word_plate_datas = []
                                for word_plate_data in word_plate_datas:
                                    if len(word_plate_data) > 0:
                                        player_word_plate_datas.append(int(word_plate_data, 16))
                                    
                                self.player_word_plate_datas.append(player_word_plate_datas)                
    
        return True
    
    def WriteJson(self, path):
        
        heap_word_plate_datas = []
        for word_plate_data in self.heap_word_plate_datas:
            heap_word_plate_datas.append("0x{:0>2X}".format(word_plate_data))
        heap_word_plate_datas = ",".join(heap_word_plate_datas)
            
        player_word_plate_datas = []
        if self.word_plate_player_count > 0:
            for seat_id in range(self.word_plate_player_count):
                if seat_id < len(self.player_word_plate_datas):            
                    one_player_word_plate_datas = self.player_word_plate_datas[seat_id]
                    if len(one_player_word_plate_datas) > 0:
                        word_plate_datas = []
                        for word_plate_data in one_player_word_plate_datas:
                            word_plate_datas.append("0x{:0>2X}".format(word_plate_data))
                        one_player_word_plate_datas = ",".join(word_plate_datas)
                        player_word_plate_datas.append(one_player_word_plate_datas)
            
        config = { 
            "Options" : {
                "player_count" : self.word_plate_player_count,
                "banker_seat_id" : self.word_plate_banker_seat_id,
                "test_count" : self.word_plate_test_count,
                "total_count" : self.word_plate_total_count,
                "everyone_count": self.word_plate_everyone_count
            }, 
            "WordPlateDatas" : {
                "heap_word_plate_datas" : heap_word_plate_datas,
                "player_word_plate_datas" : player_word_plate_datas
            } 
        }
        
        try:
            fp = open(path, 'w')
        except:
            print("open json file error!")
            return False
            
        with fp:
            try:
                json.dump(config, fp, indent=4, separators=(',',': '))
            except BaseException as err:
                print("json write error", err)
                return False, err
                
        return True    
    
        
#----------------------------------------------------------------------

class DragShape:
    
    def __init__(self, bmp = None):
        
        self.pos = wx.Point()
        self.shown = True
        self.fullscreen = False
        self.bmp = None
        
    def SetBitmap(self, bmp):
        
        self.bmp = bmp
        
    def SetPos(self, pt):
        
        self.pos = pt
        
    def GetPos(self):
        
        return self.pos
    
    def GetPosX(self):
        
        return self.pos.x
    
    def GetPosY(self):
        
        return self.pos.y
    
    def GetWidth(self):
        
        return self.GetRect().GetWidth()
    
    def GetHeight(self):
        
        return self.GetRect().GetHeight()
    
    def GetSize(self):
        
        return self.GetRect().GetSize()
        
    def GetRect(self):
        
        if self.bmp == None:
            return wx.Rect(self.pos.x, self.pos.y, 1, 1)
        
        return wx.Rect(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight())
    
    def HitTest(self, pt):
        
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)
    

    def Draw(self, dc, op = wx.COPY):
        
        if self.bmp != None and self.bmp.Ok():
            if False:
                dc.DrawBitmap(self.bmp, self.pos.x, self.pos.y, True)
            else:
                mem_dc = wx.MemoryDC()
                mem_dc.SelectObject(self.bmp)
                dc.Blit(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight(), mem_dc, 0, 0, op, True)

            return True
        else:
            return False



WORD_PLATE_MAX_INDEX = 10 + 10 + 1
WORD_PLATE_MASK_COLOR = 0xF0
WORD_PLATE_MASK_VALUE = 0x0F

WordPlateType_Unknow = 0
WordPlateType_Heap = 1
WordPlateType_Left = 2
WordPlateType_Top = 3
WordPlateType_Right = 4
WordPlateType_Bottom = 5



class DragWordPlate(DragShape):
    
    def __init__(self, word_plate_data, word_plate_type = WordPlateType_Unknow):
        
        DragShape.__init__(self)
        
        self.fullscreen = False
        self.word_plate_data = 0
        self.word_plate_type = word_plate_type
        self.SetWordPlateData(word_plate_data)
        
    def  GetWordPlateData(self):
        
        return self.word_plate_data
        
    def GetWordPlateType(self):
        
        return self.word_plate_type
        
    def SetWordPlateData(self, word_plate_data):
        
        try:
            self._SetWordPlateImage(word_plate_data)
        except:
            print("set word_plate image exception!")
            
        self.word_plate_data = word_plate_data
        
        
    def _SetWordPlateImage(self, word_plate_data):
        
        assert(False)
        pass
        

# 牌堆字牌        
class HeapWordPlate(DragWordPlate):
    
    def __init__(self, word_plate_data):
        
        DragWordPlate.__init__(self, word_plate_data, WordPlateType_Heap)
        

    def _SetWordPlateImage(self, word_plate_data):
        
        if self.word_plate_data == word_plate_data:
            return 
        
        if word_plate_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((word_plate_data & WORD_PLATE_MASK_COLOR) >> 4) & 0xFF)
        value = ((word_plate_data & WORD_PLATE_MASK_VALUE) & 0xFF)
        file_name = 'wp.png'
        if color == 0 :
            file_name = "xx_%d.png" % (value)
        elif color == 1: 
            file_name = "dd_%d.png" % (value)
        elif color == 2 and value == 1:
            file_name =  "magic.png"
        
        word_plate_img = wx.Image('images/heap_normal/%s' % (file_name))
        word_plate_img = word_plate_img.Scale(word_plate_img.GetWidth() * 0.5, word_plate_img.GetHeight() * 0.5)  
        word_plate_bmp = wx.EmptyBitmapRGBA(word_plate_img.GetWidth(), word_plate_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(word_plate_bmp)  
        mem_dc.DrawBitmap(word_plate_img.ConvertToBitmap(), 0, 0, True)           
        self.SetBitmap(word_plate_bmp)        
    
         
# 左边字牌    
class LeftWordPlate(DragWordPlate):
    
    def __init__(self, word_plate_data):
        
        DragWordPlate.__init__(self, word_plate_data, WordPlateType_Left)
    
        
    def _SetWordPlateImage(self, word_plate_data):     
    
        if self.word_plate_data == word_plate_data:
            return 
        
        if word_plate_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((word_plate_data & WORD_PLATE_MASK_COLOR) >> 4) & 0xFF)
        value = ((word_plate_data & WORD_PLATE_MASK_VALUE) & 0xFF)
        file_name = 'wp.png'
        if color == 0 :
            file_name = "b_%d.png" % (value)
        elif color == 1: 
            file_name = "a_%d.png" % (value)
        elif color == 2 and value == 1:
            file_name =  "magic.png"
        
        word_plate_img = wx.Image('images/hand_small/%s' % (file_name))    
        word_plate_bmp = wx.EmptyBitmapRGBA(word_plate_img.GetWidth(), word_plate_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(word_plate_bmp)  
        mem_dc.DrawBitmap(word_plate_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(word_plate_bmp)
        
        
# 上面字牌
class TopWordPlate(DragWordPlate):
    
    def __init__(self, word_plate_data):
        
        DragWordPlate.__init__(self, word_plate_data, WordPlateType_Top)
        
        
    def _SetWordPlateImage(self, word_plate_data):   
        
        if self.word_plate_data == word_plate_data:
            return 
        
        if word_plate_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((word_plate_data & WORD_PLATE_MASK_COLOR) >> 4) & 0xFF)
        value = ((word_plate_data & WORD_PLATE_MASK_VALUE) & 0xFF)
        file_name = 'wp.png'
        if color == 0 :
            file_name = "b_%d.png" % (value)
        elif color == 1: 
            file_name = "a_%d.png" % (value)
        elif color == 2 and value == 1:
            file_name =  "magic.png"
        
        word_plate_img = wx.Image('images/hand_small/%s' % (file_name))    
        word_plate_bmp = wx.EmptyBitmapRGBA(word_plate_img.GetWidth(), word_plate_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(word_plate_bmp)  
        mem_dc.DrawBitmap(word_plate_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(word_plate_bmp)
        
         
# 右边字牌  
class RightWordPlate(DragWordPlate):
    
    def __init__(self, word_plate_data):
        
        DragWordPlate.__init__(self, word_plate_data, WordPlateType_Right)
    
        
    def _SetWordPlateImage(self, word_plate_data):   
        
        if self.word_plate_data == word_plate_data:
            return 
        
        if word_plate_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((word_plate_data & WORD_PLATE_MASK_COLOR) >> 4) & 0xFF)
        value = ((word_plate_data & WORD_PLATE_MASK_VALUE) & 0xFF)
        file_name = 'wp.png'
        if color == 0 :
            file_name = "b_%d.png" % (value)
        elif color == 1: 
            file_name = "a_%d.png" % (value)
        elif color == 2 and value == 1:
            file_name =  "magic.png"
        
        word_plate_img = wx.Image('images/hand_small/%s' % (file_name))    
        word_plate_bmp = wx.EmptyBitmapRGBA(word_plate_img.GetWidth(), word_plate_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(word_plate_bmp)  
        mem_dc.DrawBitmap(word_plate_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(word_plate_bmp)
        
      
# 底部字牌   
class BottomWordPlate(DragWordPlate):
    
    def __init__(self, word_plate_data):
        
        DragWordPlate.__init__(self, word_plate_data, WordPlateType_Bottom)
        
        
    def _SetWordPlateImage(self, word_plate_data):   
        
        if self.word_plate_data == word_plate_data:
            return 
        
        if word_plate_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((word_plate_data & WORD_PLATE_MASK_COLOR) >> 4) & 0xFF)
        value = ((word_plate_data & WORD_PLATE_MASK_VALUE) & 0xFF)
        file_name = 'wp.png'
        if color == 0 :
            file_name = "x_%d.png" % (value)
        elif color == 1: 
            file_name = "d_%d.png" % (value)
        elif color == 2 and value == 1:
            file_name =  "magic.png"
        
        word_plate_img = wx.Image('images/hand_big/%s' % (file_name))
        word_plate_img = word_plate_img.Scale(word_plate_img.GetWidth() * 0.5, word_plate_img.GetHeight() * 0.5)
        word_plate_bmp = wx.EmptyBitmapRGBA(word_plate_img.GetWidth(), word_plate_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(word_plate_bmp)  
        mem_dc.DrawBitmap(word_plate_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(word_plate_bmp)
 
 
SeatDirection_Left = 0
SeatDirection_Top = 1
SeatDirection_Right = 2
SeatDirection_Bottom = 3


# 堆立字牌
class PlaneHeapWordPlate:
    
    def __init__(self, parent, word_plate_datas = []):
        
        self.parent = parent
        self.shown = True
        self.layout_mode = wx.ALIGN_INVALID
        self.view_rect = wx.Rect()     
        self.display_col_count = 16
        self.word_plate_views = []
        
        self.InitWordPlateView(word_plate_datas)
    
    
    def SetHeapWordPlates(self, word_plate_datas):

        word_plate_count =  len(word_plate_datas)
        if word_plate_count > 0:
            for index in range(word_plate_count):
                word_plate_data = word_plate_datas[index]
                if index < len(self.word_plate_views):
                    self.word_plate_views[index].SetWordPlateData(word_plate_data)
                else:
                    word_plate_view = HeapWordPlate(word_plate_data)
                    self.word_plate_views.append(word_plate_view) 
                    self.parent.AddShape(word_plate_view)
                    
        if len(self.word_plate_views) > word_plate_count:
            for index in range(word_plate_count, len(self.word_plate_views)):
                self.parent.RemoveShape(self.word_plate_views[index])
            del self.word_plate_views[word_plate_count:]
            

        return True


    def SetHeapMahJong(self, index, word_plate_data):

        if index < len(self.word_plate_views):
            self.word_plate_views[index].SetWordPlateData(word_plate_data) 
            return True

        return False

    def GetHeapWordPlates(self):

        word_plate_datas = []
        for word_plate_view in self.word_plate_views:
            data = word_plate_view.GetWordPlateData()
            word_plate_datas.append(data)

        return word_plate_datas


    def GetHeapWordPlate(self, index):

        word_plate_data = 0
        if index < len(self.word_plate_views):
            word_plate_data = self.word_plate_views[index].GetWordPlateData()

        return word_plate_data

    def InitWordPlateView(self, word_plate_datas):

        for word_plate_data in word_plate_datas:
            word_plate_view = HeapWordPlate(word_plate_data)
            self.word_plate_views.append(word_plate_view) 
            self.parent.AddShape(word_plate_view)  

        self.UpdateView()
        

    def IsShow(self):
        
        return self.shown
    
    def IsHide(self):
        
        return not self.shown
    
    def SetShow(self):
        
        self.shown = True
        
    def SetHide(self):
        
        self.shown =  False
    
    def SetPosition(self, pt, mode = None):
        
        self.view_rect.SetPosition(pt)
        self.layout_mode = mode or self.layout_mode
        self.UpdateView()
        

    def UpdateView(self):

        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER:
            x -= self.view_rect.GetWidth() / 2
            y -= self.view_rect.GetHeight() / 2
        else:
            if self.layout_mode &  wx.ALIGN_CENTER_HORIZONTAL:
                x -= self.view_rect.GetWidth() / 2
            if self.layout_mode &  wx.ALIGN_CENTER_VERTICAL:
                y -= self.view_rect.GetHeight() / 2
                
        h_space = 0
        v_space = -40
        x_count = 0
        y_count = 0
        view_rect =  wx.Rect()
        for word_plate_view in self.word_plate_views:
            word_plate_view.SetPos(wx.Point(x + x_count * (word_plate_view.GetWidth() + h_space), y + y_count * (word_plate_view.GetHeight() + v_space)))
            view_rect.Union(word_plate_view.GetRect())
            x_count += 1
            if x_count >= self.display_col_count:
                x_count = 0
                y_count += 1

        self.view_rect =  view_rect
        self.parent.RefreshRect(self.view_rect)
        
    def Draw(self, dc, op = wx.COPY):
        
        pass        
        
            

INVALID_SEAT_ID = 0xFFFF
NORMAL_WORD_PLATE_COUNT = 14

# 手上字牌
class HandWordPlate:
    
    def __init__(self, parent, seat_direction, seat_id = INVALID_SEAT_ID, word_plate_datas = []):
        
        self.parent = parent
        self.shown = True
        self.seat_id = seat_id
        self.seat_direction = seat_direction
        self.partition_h = 14
        self.partition_v = 16
        self.layout_mode = wx.ALIGN_INVALID
        self.view_rect = wx.Rect()
        self.word_plate_views = []
             
        self.InitWordPlateView(word_plate_datas)
            
    def GetSeatDirection(self):
        
        return self.seat_direction
    
    def GetSeatID(self):
        
        return self.seat_id
    
    def SetSeatID(self,  seat_id):
        
        self.seat_id =  seat_id
    
    def SetHandWordPlates(self, word_plate_datas):
        
        word_plate_count =  len(word_plate_datas)
        if word_plate_count > 0:
            reverse_word_plate_datas = []
            if self.seat_direction == SeatDirection_Top or self.seat_direction ==  SeatDirection_Right:
                for word_plate_data in reversed(word_plate_datas):
                    reverse_word_plate_datas.append(word_plate_data)
                
            for index in range(word_plate_count):
                word_plate_data = word_plate_datas[index]
                if len(reverse_word_plate_datas) > 0:
                    word_plate_data = reverse_word_plate_datas[index]
                if index < len(self.word_plate_views):
                    self.word_plate_views[index].SetWordPlateData(word_plate_data)
                else:
                    if self.seat_direction == SeatDirection_Left:
                        word_plate_view = LeftWordPlate(word_plate_data)
                    elif self.seat_direction == SeatDirection_Top:
                        word_plate_view = TopWordPlate(word_plate_data)
                    elif self.seat_direction == SeatDirection_Right:
                        word_plate_view = RightWordPlate(word_plate_data)
                    else:
                        word_plate_view = BottomWordPlate(word_plate_data)                        
                    self.word_plate_views.append(word_plate_view) 
                    self.parent.AddShape(word_plate_view)
                    
        if len(self.word_plate_views) > word_plate_count:
            for index in range(word_plate_count, len(self.word_plate_views)):
                self.parent.RemoveShape(self.word_plate_views[index])            
            del self.word_plate_views[word_plate_count:]
            
            return True
        
        return False
        
    def SetHandMahJong(self, index, word_plate_data):
        
        if index < len(self.word_plate_views):
            self.word_plate_views[index].SetWordPlateData(word_plate_data) 
            return True
        
        return False
    
    def GetHandWordPlates(self):
        
        word_plate_datas = []
        for word_plate_view in self.word_plate_views:
            data = word_plate_view.GetWordPlateData()
            word_plate_datas.append(data)
        
        if self.seat_direction == SeatDirection_Top or self.seat_direction ==  SeatDirection_Right:
            word_plate_datas.reverse()
            
        return word_plate_datas
    
    
    def GetHandWordPlate(self, index):
        
        word_plate_data = 0
        if index < len(self.word_plate_views):
            word_plate_data = self.word_plate_views[index].GetWordPlateData()
            
        return word_plate_data
    
    def InitWordPlateView(self, word_plate_datas):
        
        if self.seat_direction == SeatDirection_Left:
            self.InitLeftWordPlateView(word_plate_datas)
        elif self.seat_direction == SeatDirection_Top:
            reverse_word_plate_datas = []
            for word_plate_data in reversed(word_plate_datas):
                reverse_word_plate_datas.append(word_plate_data)          
            self.InitTopWordPlateView(reverse_word_plate_datas)
        elif self.seat_direction == SeatDirection_Right:
            reverse_word_plate_datas = []
            for word_plate_data in reversed(word_plate_datas):
                reverse_word_plate_datas.append(word_plate_data)
            self.InitRightWordPlateView(reverse_word_plate_datas)
        else:
            self.InitBottomWordPlateView(word_plate_datas)
            
        self.UpdateView()
            
    
    def InitLeftWordPlateView(self, word_plate_datas):
        
        for word_plate_data in word_plate_datas:
            word_plate_view = LeftWordPlate(word_plate_data)
            self.word_plate_views.append(word_plate_view) 
            self.parent.AddShape(word_plate_view)  
            
        
    def InitTopWordPlateView(self, word_plate_datas):                    
                   
        for word_plate_data in word_plate_datas:
            word_plate_view = TopWordPlate(word_plate_data)
            self.word_plate_views.append(word_plate_view) 
            self.parent.AddShape(word_plate_view)  
                
                
    def InitRightWordPlateView(self, word_plate_datas):
     
        for word_plate_data in word_plate_datas:
            word_plate_view = RightWordPlate(word_plate_data)
            self.word_plate_views.append(word_plate_view) 
            self.parent.AddShape(word_plate_view)  
        
                
    def InitBottomWordPlateView(self, word_plate_datas):
        
        for word_plate_data in word_plate_datas:
            word_plate_view = BottomWordPlate(word_plate_data)
            self.word_plate_views.append(word_plate_view) 
            self.parent.AddShape(word_plate_view)      
     
    def IsShow(self):
        
        return self.shown
    
    def IsHide(self):
        
        return not self.shown
    
    def SetShow(self):
        
        self.shown = True
        
    def SetHide(self):
        
        self.shown =  False     
            
    def SetPosition(self, pt, mode = None):
        
        self.view_rect.SetPosition(pt)
        self.layout_mode = mode or self.layout_mode
        self.UpdateView()
        
    def GetRect(self):
        
        return self.view_rect
                
    def UpdateView(self):
       
        if self.seat_direction == SeatDirection_Left:
            self.UpdateLeftWordPlateView()
        elif self.seat_direction == SeatDirection_Top:
            self.UpdateTopWordPlateView()
        elif self.seat_direction == SeatDirection_Right:
            self.UpdateRightWordPlateView()
        else:
            self.UpdateBottomWordPlateView() 
            
        self.parent.RefreshRect(self.view_rect)
        
        
    def UpdateLeftWordPlateView(self):

        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_VERTICAL:
            y -= self.view_rect.GetHeight() / 2 
        v_space = -12
        count = 0
        view_rect =  wx.Rect()
        for word_plate_view in self.word_plate_views:
            word_plate_view.SetPos(wx.Point(x, y + count * (word_plate_view.GetHeight() + v_space) + (0 if count + 1 <= NORMAL_WORD_PLATE_COUNT else self.partition_v)))
            view_rect.Union(word_plate_view.GetRect())
            count += 1
            
        self.view_rect =  view_rect
    
        
    def UpdateTopWordPlateView(self):                    
            
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_HORIZONTAL:
            x -= self.view_rect.GetWidth() / 2          
        h_space = -1  
        count = 0
        view_rect =  wx.Rect()
        word_plate_count = len(self.word_plate_views)
        for word_plate_view in self.word_plate_views:
            word_plate_view.SetPos(wx.Point(x + count * (word_plate_view.GetWidth() + h_space) + (0 if not (count > 0 and word_plate_count > NORMAL_WORD_PLATE_COUNT) else self.partition_h), y))
            view_rect.Union(word_plate_view.GetRect())
            count += 1
                
        self.view_rect =  view_rect
                
    def UpdateRightWordPlateView(self):
     
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_VERTICAL:
            y -= self.view_rect.GetHeight() / 2        
        v_space = -12
        count = 0
        view_rect =  wx.Rect()
        word_plate_count = len(self.word_plate_views)
        for word_plate_view in self.word_plate_views:
            word_plate_view.SetPos(wx.Point(x, y + count * (word_plate_view.GetHeight() + v_space) + (0 if not (count > 0 and word_plate_count > NORMAL_WORD_PLATE_COUNT) else self.partition_v)))
            view_rect.Union(word_plate_view.GetRect())
            count += 1
        
        self.view_rect =  view_rect
                
    def UpdateBottomWordPlateView(self):   
        
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_HORIZONTAL:
            x -= self.view_rect.GetWidth() / 2          
        h_space = 0  
        count = 0
        view_rect =  wx.Rect()
        for word_plate_view in self.word_plate_views:
            word_plate_view.SetPos(wx.Point(x + count * (word_plate_view.GetWidth() + h_space) + (0 if count + 1 <= NORMAL_WORD_PLATE_COUNT else self.partition_h), y))
            view_rect.Union(word_plate_view.GetRect())
            count += 1      

        self.view_rect =  view_rect
        
        
    def Draw(self, dc, op = wx.COPY):
        
        pass
        
#----------------------------------------------------------------------

class DragCanvas(wx.Panel):
    
    def __init__(self, parent, ID = -1):
        
        wx.Panel.__init__(self, parent, ID)
        
        self.parent = parent
        self.shapes = []
        self.drag_image = None
        self.drag_shape = None 

        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)       
        #self.SetBackgroundColour(wx.Colour(255,255,255))
        
        self.bmp_bg = None
        self.bg_image = wx.Image('images/wp_bg/room_bg.png')
        self.AdjustBackground()

        # init word plate view
        self.InitWordPlateView()
        self.UpdateWordPlateView()
        
        # add event
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
    def InitWordPlateView(self):
        
        config = self.parent.config

        self.plane_heap_word_plate = PlaneHeapWordPlate(self, config.heap_word_plate_datas)
        self.hand_word_plate_ctrls = []
                    
        seat_directions =  [SeatDirection_Left, SeatDirection_Top,  SeatDirection_Right, SeatDirection_Bottom]
        for seat_direction in seat_directions:
            display = False
            seat_id = INVALID_SEAT_ID
            player_word_plate_datas = []
            if config.word_plate_player_count == 1:
                if seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id =  0
            elif config.word_plate_player_count == 2:
                if seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 1                    
            elif config.word_plate_player_count == 3:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 2                    
            elif config.word_plate_player_count == 4:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 2                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 3                  
            else:
                display =  False

            if seat_id < len(config.player_word_plate_datas):   
                player_word_plate_datas = config.player_word_plate_datas[seat_id]     
            
            word_plate_view = HandWordPlate(self, seat_direction, seat_id, player_word_plate_datas)
            if display ==  True:
                word_plate_view.SetShow()
            else:
                word_plate_view.SetHide()
            self.hand_word_plate_ctrls.append(word_plate_view)
                
                
                
    def ResetWordPlateView(self):
                
        config = self.parent.config
    
        self.plane_heap_word_plate.SetHeapWordPlates(config.heap_word_plate_datas)
        self.plane_heap_word_plate.UpdateView()
        
        for word_plate_view in self.hand_word_plate_ctrls:
            display = False
            seat_id = INVALID_SEAT_ID
            player_word_plate_datas = []
            seat_direction = word_plate_view.seat_direction
            if config.word_plate_player_count == 1:
                if seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id =  0
            elif config.word_plate_player_count == 2:
                if seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 1                    
            elif config.word_plate_player_count == 3:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 2                    
            elif config.word_plate_player_count == 4:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 2                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 3                  
            else:
                display =  False
                
            if seat_id < len(config.player_word_plate_datas):   
                player_word_plate_datas = config.player_word_plate_datas[seat_id]             
                
            word_plate_view.SetSeatID(seat_id)
            word_plate_view.SetHandWordPlates(player_word_plate_datas)
            if display == True:
                word_plate_view.SetShow()
            else:
                word_plate_view.SetHide()
            word_plate_view.UpdateView()
                
    def SaveWordPlateViewToConfig(self):
        
        config = self.parent.config
        
        if self.plane_heap_word_plate.IsShow():
            config.heap_word_plate_datas = self.plane_heap_word_plate.GetHeapWordPlates()
        else:
            config.heap_word_plate_datas = []
        
        for word_plate_view in self.hand_word_plate_ctrls:
            player_word_plate_datas = []
            seat_id = word_plate_view.GetSeatID()
            if word_plate_view.IsShow():
                player_word_plate_datas =  word_plate_view.GetHandWordPlates()
                
            if seat_id < config.word_plate_player_count and seat_id < len(config.player_word_plate_datas):
                config.player_word_plate_datas[seat_id] = player_word_plate_datas
        
        if config.word_plate_test_count <= 0:
            config.word_plate_test_count = 1
    
    def UpdateWordPlateView(self):
        
        client_size = self.GetClientSize()
        center_point_x = client_size.GetWidth() / 2
        center_point_y = client_size.GetHeight() / 2 - 10
        self.plane_heap_word_plate.SetPosition(wx.Point(center_point_x, center_point_y), wx.ALIGN_CENTER)   
        
        for word_plate_view in self.hand_word_plate_ctrls:
            if word_plate_view.seat_direction == SeatDirection_Left:
                word_plate_view.SetPosition(wx.Point(30, center_point_y + 10), wx.ALIGN_CENTER_VERTICAL)
            elif word_plate_view.seat_direction == SeatDirection_Top:
                word_plate_view.SetPosition(wx.Point(center_point_x, 30), wx.ALIGN_CENTER_HORIZONTAL)
            elif word_plate_view.seat_direction == SeatDirection_Right:
                word_plate_view.SetPosition(wx.Point(client_size.GetWidth() - word_plate_view.GetRect().GetWidth() - 30, center_point_y + 10), wx.ALIGN_CENTER_VERTICAL)
            elif word_plate_view.seat_direction == SeatDirection_Bottom:
                word_plate_view.SetPosition(wx.Point(center_point_x, client_size.GetHeight() - word_plate_view.GetRect().GetHeight() - 30), wx.ALIGN_CENTER_HORIZONTAL)
        
        self.Refresh()
        
        
    def AdjustBackground(self):
        
        size = self.GetClientSize()
        bg_size = self.bg_image.GetSize()
        if size.width != 0 and size.height != 0 and size != bg_size:
            image = self.bg_image.Scale(size.width, size.height)
            self.bmp_bg = image.ConvertToBitmap() 
        
        
    def AddShape(self, shape):
        
        is_exist =  False
        for _shape in self.shapes:
            if _shape is shape:
                is_exist =  True
                break
            
        if is_exist == False:
            self.shapes.append(shape)
    
    def RemoveShape(self, shape):
        
        index =  0
        for _shape in self.shapes:
            if _shape is shape:
                del self.shapes[index]
                return True
            
            index += 1
            
        return False
    
        
    def ClearShape(self):
        
        self.shapes =  []
    
    def FindShape(self, pt):
        
        for shape in reversed(self.shapes):
            if shape.HitTest(pt) and shape.shown == True:
                return shape  
            
        return None    
        
    # window size
    def OnSize(self, evt):
        
        self.AdjustBackground()         
        self.UpdateWordPlateView()
        
        evt.Skip()

    # We're not doing anything here, but you might have reason to.
    # for example, if you were dragging something, you might elect to
    # 'drop it' when the cursor left the window.
    def OnLeaveWindow(self, evt):
        pass


    # tile the background bitmap
    def TileBackground(self, dc):
        
        sz = self.GetClientSize()
        x = 0
        y = 0
        
        if self.bmp_bg != None:
            dc.DrawBitmap(self.bmp_bg, 0, 0, True)


    # Go through our list of shapes and draw them in whatever place they are.
    def DrawShapes(self, dc):
        
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)

    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.TileBackground(dc)

    # Fired whenever a paint event occurs
    def OnPaint(self, evt):
        
        dc = wx.PaintDC(self)
        self.DrawShapes(dc)

    # Left mouse button is down.
    def OnLeftDown(self, evt):

        shape = self.FindShape(evt.GetPosition())
        if shape:
            self.drag_shape = shape
            self.dragStartPos = evt.GetPosition()

    # Left mouse button up.
    def OnLeftUp(self, evt):
        
        if not self.drag_image or not self.drag_shape:
            self.drag_image = None
            self.drag_shape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.drag_image.Hide()
        self.drag_image.EndDrag()
        self.drag_image = None

        shape = self.FindShape(evt.GetPosition())
        if shape:        
            word_plate_data1 = shape.GetWordPlateData()
            word_plate_data2 = self.drag_shape.GetWordPlateData()
            shape.SetWordPlateData(word_plate_data2)
            self.drag_shape.SetWordPlateData(word_plate_data1)
    
            self.drag_shape.shown = True      
            self.RefreshRect(shape.GetRect())
            self.RefreshRect(self.drag_shape.GetRect())
            self.drag_shape = None            
        else:
            self.drag_shape.shown = True
            self.RefreshRect(self.drag_shape.GetRect())
            self.drag_shape = None


    # The mouse is moving
    def OnMotion(self, evt):
        # Ignore mouse movement if we're not dragging.
        if not self.drag_shape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.drag_shape and not self.drag_image:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = evt.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.drag_shape.shown = False
            self.RefreshRect(self.drag_shape.GetRect(), True)
            self.Update()

            self.drag_image = wx.DragImage(self.drag_shape.bmp, wx.StockCursor(wx.CURSOR_HAND))
            hotspot = self.dragStartPos - self.drag_shape.pos
            self.drag_image.BeginDrag(hotspot, self, self.drag_shape.fullscreen)
            self.drag_image.Show()
            self.drag_image.Move(pt)
    
        elif self.drag_shape and self.drag_image:
            
            # move drag image to position
            self.drag_image.Move(evt.GetPosition())
            
    
    
class WordPlateSettingDlg(wx.Dialog):
    
    def __init__(self, parent = None, id = -1,):
        
        wx.Dialog.__init__(self, parent, id, title=u"字牌设置", size=(640, 530))
        
        self.parent = parent
        self.panel = wx.Panel(self)
        frame_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panel.SetSizer(frame_sizer)        
        
        static_box = wx.StaticBox(self.panel, label=u"字牌游戏配置：")
        static_box_sizer = wx.StaticBoxSizer(static_box, orient=wx.HORIZONTAL)
        frame_sizer.Add(static_box_sizer, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 6)
        
        label_word_plate_total_count = wx.StaticText(static_box, label = u"字牌总数目：")
        self.spin_word_plate_total_count = wx.SpinCtrl(static_box, value='84', size=(60,-1))    
        self.spin_word_plate_total_count.SetRange(0, 84)
        self.spin_word_plate_total_count.SetValue(80)
        self.spin_word_plate_total_count.Disable()
        static_box_sizer.Add(label_word_plate_total_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        static_box_sizer.Add(self.spin_word_plate_total_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)
        
        label_word_plate_player_count = wx.StaticText(static_box, label = u"游戏人数：")
        self.spin_word_plate_player_count = wx.SpinCtrl(static_box, value='4', size=(40,-1))    
        self.spin_word_plate_player_count.SetRange(2, 4)
        self.spin_word_plate_player_count.SetValue(4)
        static_box_sizer.Add(label_word_plate_player_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_word_plate_player_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)
        
        label_word_plate_everyone_count = wx.StaticText(static_box, label = u"每人牌数：")
        self.choice_word_plate_everyone_count = wx.Choice(static_box, size=(40,-1), choices= ['14', '17', '20'])    
        self.choice_word_plate_everyone_count.Select(0)
        static_box_sizer.Add(label_word_plate_everyone_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.choice_word_plate_everyone_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)        
        
        label_word_plate_banker_seat_id = wx.StaticText(static_box, label = u"庄家座位：")
        self.spin_word_plate_banker_seat_id = wx.SpinCtrl(static_box, value='0', size=(40,-1))    
        self.spin_word_plate_banker_seat_id.SetRange(0, 3)
        self.spin_word_plate_banker_seat_id.SetValue(0)
        static_box_sizer.Add(label_word_plate_banker_seat_id, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_word_plate_banker_seat_id, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)
        
        label_word_plate_test_count = wx.StaticText(static_box, label = u"测试次数：")
        self.spin_word_plate_test_count = wx.SpinCtrl(static_box, value='1', size=(50,-1))    
        self.spin_word_plate_test_count.SetRange(0, 1000)
        self.spin_word_plate_test_count.SetValue(1)
        static_box_sizer.Add(label_word_plate_test_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_word_plate_test_count, 0, wx.ALIGN_CENTER_VERTICAL)          
        
        
        static_box1 = wx.StaticBox(self.panel, label=u"字牌数目配置：")
        static_box_sizer1 = wx.StaticBoxSizer(static_box1, orient=wx.VERTICAL)
        frame_sizer1_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        static_box_sizer1.AddSpacer(12)
        static_box_sizer1.Add(frame_sizer1_1)
        static_box_sizer1.AddSpacer(20)
        static_box_sizer1.Add(frame_sizer1_2)
        static_box_sizer1.AddSpacer(20)
        static_box_sizer1.Add(frame_sizer1_3)
        static_box_sizer1.AddSpacer(6)
        frame_sizer.Add(static_box_sizer1, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 6)
        
        label_word_plate_type_small  = wx.StaticText(static_box1, label = u"小写字牌：")
        label_word_plate_type_big = wx.StaticText(static_box1, label = u"大写字牌：")
        label_word_plate_type_magic = wx.StaticText(static_box1, label = u"癞子字牌：")
        font = label_word_plate_type_small.GetFont()
        font.SetPointSize(11) 
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label_word_plate_type_small.SetFont(font)
        label_word_plate_type_big.SetFont(font)
        label_word_plate_type_magic.SetFont(font)
        frame_sizer1_1.Add(label_word_plate_type_small, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        frame_sizer1_2.Add(label_word_plate_type_big, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)
        frame_sizer1_3.Add(label_word_plate_type_magic, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 6)

        self.word_plate_small_list = []
        self.word_plate_big_list = []
        self.word_plate_magic_list = []
        
        for i in range(10):
        
            file_name = "xx_%d.png" % (i+1)
            word_plate_img = wx.Image('images/heap_normal/%s' % (file_name))
            word_plate_bmp = self.ImageMerge(word_plate_img)            
            img_word_plate = wx.StaticBitmap(static_box1, bitmap=word_plate_bmp)
            spin_word_plate_count = wx.SpinCtrl(static_box1, size=(word_plate_bmp.GetWidth() + 6,-1), value='4', min=0, max=4)
            self.word_plate_small_list.append({"image": img_word_plate, "word_plate_data": i+1, "word_plate_count": spin_word_plate_count})
            word_plate_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            word_plate_sizer.Add(img_word_plate, 0, wx.CENTER)
            word_plate_sizer.Add(spin_word_plate_count, 0, wx.CENTER)
            frame_sizer1_1.Add(word_plate_sizer)
            frame_sizer1_1.AddSpacer(10)
            
            file_name = "dd_%d.png" % (i+1)
            word_plate_img = wx.Image('images/heap_normal/%s' % (file_name))
            word_plate_bmp = self.ImageMerge(word_plate_img)               
            img_word_plate = wx.StaticBitmap(static_box1, bitmap=word_plate_bmp)
            spin_word_plate_count = wx.SpinCtrl(static_box1, size=(word_plate_bmp.GetWidth() + 6,-1), value='4', min=0, max=4)
            self.word_plate_big_list.append({"image": img_word_plate, "word_plate_data": 0x10+i+1, "word_plate_count": spin_word_plate_count})
            word_plate_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            word_plate_sizer.Add(img_word_plate, 0, wx.CENTER)
            word_plate_sizer.Add(spin_word_plate_count, 0, wx.CENTER)
            frame_sizer1_2.Add(word_plate_sizer)
            frame_sizer1_2.AddSpacer(10)


        for i in range(1):
            file_name = "magic.png" 
            word_plate_img = wx.Image('images/heap_normal/%s' % (file_name))
            word_plate_bmp = self.ImageMerge(word_plate_img)               
            img_word_plate = wx.StaticBitmap(static_box1, bitmap=word_plate_bmp)
            spin_word_plate_count = wx.SpinCtrl(static_box1, size=(word_plate_bmp.GetWidth() + 6,-1), value='0', min=0, max=4)
            self.word_plate_magic_list.append({"image": img_word_plate, "word_plate_data": 0x20+i+1, "word_plate_count": spin_word_plate_count})
            word_plate_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            word_plate_sizer.Add(img_word_plate, 0, wx.CENTER)
            word_plate_sizer.Add(spin_word_plate_count, 0, wx.CENTER)
            frame_sizer1_3.Add(word_plate_sizer)
            frame_sizer1_3.AddSpacer(10)       
            
        
        self.check_all_word_plate_small = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_word_plate_big = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_word_plate_magic = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_word_plate_small.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_word_plate_big.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_word_plate_magic.Set3StateValue(wx.CHK_UNCHECKED)        
        frame_sizer1_1.Add(self.check_all_word_plate_small, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_2.Add(self.check_all_word_plate_big, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_3.Add(self.check_all_word_plate_magic, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)        
        
        self.UpdateSettings()
        self.UpdateWordPlateTotalCount()
        
        
        # 控件事件绑定
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinWordPlateTotalCount, self.spin_word_plate_total_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinWordPlateTotalCount, self.spin_word_plate_total_count) 
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_word_plate_player_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_word_plate_player_count)        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_word_plate_banker_seat_id)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_word_plate_banker_seat_id)      
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_word_plate_test_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_word_plate_test_count)
        
        self.Bind(wx.EVT_CHOICE, self.OnChoiceValue, self.choice_word_plate_everyone_count)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_word_plate_small) 
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_word_plate_big)  
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_word_plate_magic)   
        
        for word_plate_ctrl in self.word_plate_small_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinWordPlateTotalCount, word_plate_ctrl["word_plate_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinWordPlateTotalCount, word_plate_ctrl["word_plate_count"]) 
        for word_plate_ctrl in self.word_plate_big_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinWordPlateTotalCount, word_plate_ctrl["word_plate_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinWordPlateTotalCount, word_plate_ctrl["word_plate_count"]) 
        for word_plate_ctrl in self.word_plate_magic_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinWordPlateTotalCount, word_plate_ctrl["word_plate_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinWordPlateTotalCount, word_plate_ctrl["word_plate_count"])         
   
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def ImageMerge(self, word_plate_img):
        
        word_plate_img = word_plate_img.Scale(word_plate_img.GetWidth() * 0.5, word_plate_img.GetHeight() * 0.5)  
        word_plate_bmp = wx.EmptyBitmapRGBA(word_plate_img.GetWidth(), word_plate_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(word_plate_bmp)   
        mem_dc.DrawBitmap(word_plate_img.ConvertToBitmap(), 0, 0, True)        
        
        return word_plate_bmp
    
    
    def UpdateSettings(self):
        
        self.spin_word_plate_player_count.SetValue(self.parent.config.word_plate_player_count)
        self.parent.config.word_plate_player_count = self.spin_word_plate_player_count.GetValue()
        if self.parent.config.word_plate_player_count > 0:
            self.spin_word_plate_banker_seat_id.SetRange(0, self.parent.config.word_plate_player_count - 1)
        else:
            self.spin_word_plate_banker_seat_id.SetRange(0, 0)
        
        if self.parent.config.word_plate_banker_seat_id >= self.spin_word_plate_player_count:
            self.parent.config.word_plate_banker_seat_id = self.spin_word_plate_player_count - 1
        self.spin_word_plate_banker_seat_id.SetValue(self.parent.config.word_plate_banker_seat_id)
        self.parent.config.word_plate_banker_seat_id = self.spin_word_plate_banker_seat_id.GetValue()
        
        self.spin_word_plate_test_count.SetValue(self.parent.config.word_plate_test_count if self.parent.config.word_plate_test_count != 0 else 1)
        self.parent.config.word_plate_test_count = self.spin_word_plate_test_count.GetValue()
        
        select_index = 0
        select_values = []        
        chioce_values = [14, 17, 20] if self.parent.config.word_plate_player_count < 4 else [14, 17]
        if self.parent.config.word_plate_everyone_count not in chioce_values:
            self.parent.config.word_plate_everyone_count = chioce_values[0]
            
        for index in range(len(chioce_values)):
            select_values.append(str(chioce_values[index]))
            if chioce_values[index] == self.parent.config.word_plate_everyone_count:
                select_index = index
        self.choice_word_plate_everyone_count.SetItems(select_values)
        self.choice_word_plate_everyone_count.Select(select_index)
        
        word_plate_indexs = [0 for i in range(WORD_PLATE_MAX_INDEX)]
        for word_plate_data in self.parent.config.heap_word_plate_datas:
            index = self.SwitchWordPlateToIndex(word_plate_data)
            if index < WORD_PLATE_MAX_INDEX:                
                word_plate_indexs[index] += 1
                
        for player_word_plate_datas in self.parent.config.player_word_plate_datas:
            for word_plate_data in player_word_plate_datas:
                index = self.SwitchWordPlateToIndex(word_plate_data)
                if index < WORD_PLATE_MAX_INDEX:                
                    word_plate_indexs[index] += 1                
            
        for word_plate_control in self.word_plate_small_list:
            word_plate_index = self.SwitchWordPlateToIndex(word_plate_control["word_plate_data"])
            if word_plate_index < WORD_PLATE_MAX_INDEX:
                word_plate_control["word_plate_count"].SetValue(word_plate_indexs[word_plate_index])
                
        for word_plate_control in self.word_plate_big_list:
            word_plate_index = self.SwitchWordPlateToIndex(word_plate_control["word_plate_data"])
            if word_plate_index < WORD_PLATE_MAX_INDEX:
                word_plate_control["word_plate_count"].SetValue(word_plate_indexs[word_plate_index])     
                
        for word_plate_control in self.word_plate_magic_list:
            word_plate_index = self.SwitchWordPlateToIndex(word_plate_control["word_plate_data"])
            if word_plate_index < WORD_PLATE_MAX_INDEX:
                word_plate_control["word_plate_count"].SetValue(word_plate_indexs[word_plate_index])
                
            
    @staticmethod
    def SwitchWordPlateToIndex(word_plate_data):
        
        word_plate_color = ((word_plate_data & WORD_PLATE_MASK_COLOR) >> 4) & 0xFF
        word_plate_value = (word_plate_data & WORD_PLATE_MASK_VALUE) & 0xFF
        word_plate_index = word_plate_color * 10 + word_plate_value - 1
        
        return word_plate_index
    
    def GetWordPlateDatas(self):
        
        word_plate_datas = []
        for word_plate_control in self.word_plate_small_list:
            word_plate_index = self.SwitchWordPlateToIndex(word_plate_control["word_plate_data"])
            if word_plate_index < WORD_PLATE_MAX_INDEX and word_plate_control["word_plate_count"].GetValue() > 0:
                for index in range(word_plate_control["word_plate_count"].GetValue()):
                    word_plate_datas.append(word_plate_control["word_plate_data"])
                
        for word_plate_control in self.word_plate_big_list:
            word_plate_index = self.SwitchWordPlateToIndex(word_plate_control["word_plate_data"])
            if word_plate_index < WORD_PLATE_MAX_INDEX and word_plate_control["word_plate_count"].GetValue() > 0:
                for index in range(word_plate_control["word_plate_count"].GetValue()):
                    word_plate_datas.append(word_plate_control["word_plate_data"])   
                
        for word_plate_control in self.word_plate_magic_list:
            word_plate_index = self.SwitchWordPlateToIndex(word_plate_control["word_plate_data"])
            if word_plate_index < WORD_PLATE_MAX_INDEX and word_plate_control["word_plate_count"].GetValue() > 0:
                for index in range(word_plate_control["word_plate_count"].GetValue()):
                    word_plate_datas.append(word_plate_control["word_plate_data"])
                
        return word_plate_datas
    
    def AdjustWordPlateDatas(self, word_plate_datas):
        
        config = self.parent.config
        
        if len(word_plate_datas) > 0:
            random.shuffle(word_plate_datas)
        
        config.heap_word_plate_datas = []
        config.player_word_plate_datas = []
        if config.word_plate_player_count > 0:
            
            for seat_id in range(config.word_plate_player_count):
                word_plate_count = config.word_plate_everyone_count if seat_id != config.word_plate_banker_seat_id else config.word_plate_everyone_count + 1
                if len(word_plate_datas) >= word_plate_count: 
                    player_word_plate_datas = word_plate_datas[0 : word_plate_count]
                    del word_plate_datas[0 : word_plate_count]
                    config.player_word_plate_datas.append(player_word_plate_datas)
                elif len(word_plate_datas) > 0:
                    player_word_plate_datas = word_plate_datas[0 : ]
                    del word_plate_datas[0 : ]
                    config.player_word_plate_datas.append(player_word_plate_datas)                    
                
        if len(word_plate_datas) > 0:
            for word_plate_data in word_plate_datas:
                config.heap_word_plate_datas.append(word_plate_data)
                
                
    
    def UpdateWordPlateTotalCount(self):
        
        word_plate_total_count = 0
        word_plate_small_count = 0
        word_plate_big_count = 0
        word_plate_magic_count = 0
        
        for word_plate_ctrl in self.word_plate_small_list:
            word_plate_small_count += word_plate_ctrl["word_plate_count"].GetValue()
            word_plate_total_count += word_plate_ctrl["word_plate_count"].GetValue()
            
        for word_plate_ctrl in self.word_plate_big_list:
            word_plate_big_count += word_plate_ctrl["word_plate_count"].GetValue()
            word_plate_total_count += word_plate_ctrl["word_plate_count"].GetValue()            
            
        for word_plate_ctrl in self.word_plate_magic_list:
            word_plate_magic_count += word_plate_ctrl["word_plate_count"].GetValue()
            word_plate_total_count += word_plate_ctrl["word_plate_count"].GetValue()  
            
        self.check_all_word_plate_small.Set3StateValue(wx.CHK_UNCHECKED if word_plate_small_count == 0 else (wx.CHK_CHECKED if word_plate_small_count == 10*4 else wx.CHK_UNDETERMINED))
        self.check_all_word_plate_big.Set3StateValue(wx.CHK_UNCHECKED if word_plate_big_count == 0 else (wx.CHK_CHECKED if word_plate_big_count == 10*4 else wx.CHK_UNDETERMINED))
        self.check_all_word_plate_magic.Set3StateValue(wx.CHK_UNCHECKED if word_plate_magic_count == 0 else (wx.CHK_CHECKED if word_plate_magic_count == 1*4 else wx.CHK_UNDETERMINED))            
        
        self.spin_word_plate_total_count.SetValue(word_plate_total_count)
        self.parent.config.word_plate_total_count = word_plate_total_count
        
    def OnClose(self, evt):
        
        word_plate_datas =  self.GetWordPlateDatas()
        self.AdjustWordPlateDatas(word_plate_datas)
        evt.Skip()
        
    
    def OnCheckBox(self, evt):
        
        checkbox = evt.GetEventObject()
        if checkbox is self.check_all_word_plate_small:
            for word_plate_ctrl in self.word_plate_small_list:
                word_plate_ctrl["word_plate_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)            
        elif checkbox is self.check_all_word_plate_big:
            for word_plate_ctrl in self.word_plate_big_list:
                word_plate_ctrl["word_plate_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)              
        elif checkbox is self.check_all_word_plate_magic:
            for word_plate_ctrl in self.word_plate_magic_list:
                word_plate_ctrl["word_plate_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else 4)
                
        self.UpdateWordPlateTotalCount()
        
        
    def FindWordPlateSpinCtrl(self, spin):
        
        for word_plate_ctrl in self.word_plate_small_list:
            if spin is word_plate_ctrl["word_plate_count"]:  
                return True
        for word_plate_ctrl in self.word_plate_big_list:
            if spin is word_plate_ctrl["word_plate_count"]:  
                return True
        for word_plate_ctrl in self.word_plate_magic_list:
            if spin is word_plate_ctrl["word_plate_count"]:  
                return True
            
        return False
            
        
    def OnSelectedSpinWordPlateTotalCount(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_word_plate_total_count:
            self.parent.config.word_plate_total_count = spin.GetValue()
        else:
            if self.FindWordPlateSpinCtrl(spin):
                self.UpdateWordPlateTotalCount()
        
    def OnChangeSpinWordPlateTotalCount(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_word_plate_total_count:
            self.parent.config.word_plate_total_count = spin.GetValue()        
        else:
            if self.FindWordPlateSpinCtrl(spin):
                self.UpdateWordPlateTotalCount()  
                
    def OnSelectedSpinValue(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_word_plate_player_count:
            self.parent.config.word_plate_player_count = spin.GetValue()
            if self.parent.config.word_plate_player_count > 0:
                self.spin_word_plate_banker_seat_id.SetRange(0, self.parent.config.word_plate_player_count - 1)
                if self.spin_word_plate_banker_seat_id.GetValue() >= self.parent.config.word_plate_player_count:
                    self.spin_word_plate_banker_seat_id.SetValue(self.parent.config.word_plate_player_count - 1)
                    
                select_index = 0
                select_values = []        
                chioce_values = [14, 17, 20] if self.parent.config.word_plate_player_count < 4 else [14, 17]
                if self.parent.config.word_plate_everyone_count not in chioce_values:
                    self.parent.config.word_plate_everyone_count = chioce_values[0]
                    
                for index in range(len(chioce_values)):
                    select_values.append(str(chioce_values[index]))
                    if chioce_values[index] == self.parent.config.word_plate_everyone_count:
                        select_index = index
                self.choice_word_plate_everyone_count.SetItems(select_values)
                self.choice_word_plate_everyone_count.Select(select_index)                    
            else:
                self.spin_word_plate_banker_seat_id.SetRange(0, 0)
                self.spin_word_plate_banker_seat_id.SetValue(0)
                self.choice_word_plate_everyone_count.SetItems(["14"])
                self.choice_word_plate_everyone_count.Select(0)                 
                
            self.parent.config.word_plate_banker_seat_id = self.spin_word_plate_banker_seat_id.GetValue()
            
            select_index = self.choice_word_plate_everyone_count.GetCurrentSelection()
            self.parent.config.word_plate_everyone_count = int(self.choice_word_plate_everyone_count.GetString(select_index))            
            
        elif spin is self.spin_word_plate_banker_seat_id:
            self.parent.config.word_plate_banker_seat_id = spin.GetValue() 
            
        elif spin is self.spin_word_plate_test_count:
            self.parent.config.word_plate_test_count = spin.GetValue()               
        
    def OnChangeSpinValue(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_word_plate_player_count:
            self.parent.config.word_plate_player_count = spin.GetValue()
            if self.parent.config.word_plate_player_count > 0:
                self.spin_word_plate_banker_seat_id.SetRange(0, self.parent.config.word_plate_player_count - 1)
                if self.spin_word_plate_banker_seat_id.GetValue() >= self.parent.config.word_plate_player_count:
                    self.spin_word_plate_banker_seat_id.SetValue(self.parent.config.word_plate_player_count - 1)
            else:
                self.spin_word_plate_banker_seat_id.SetRange(0, 0)
                self.spin_word_plate_banker_seat_id.SetValue(0)
                
            self.parent.config.word_plate_banker_seat_id = self.spin_word_plate_banker_seat_id.GetValue() 
            
        elif spin is self.spin_word_plate_banker_seat_id:
            self.parent.config.word_plate_banker_seat_id = spin.GetValue()  
            
        elif spin is self.spin_word_plate_test_count:
            self.parent.config.word_plate_test_count = spin.GetValue()
            
    def OnChoiceValue(self, evt):
        
        choice =  evt.GetEventObject()
        
        if choice is self.choice_word_plate_everyone_count:
            select_index = choice.GetCurrentSelection()
            self.parent.config.word_plate_everyone_count = int(choice.GetString(select_index))

    

class WordPlateMainFrame(wx.Frame):
    
    def __init__(self):
        
        wx.Frame.__init__(self, parent = None, id = -1, title = u'字牌做牌工具') 
        
        self.SetIcon(wx.Icon("images/wordplate.ico"))
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.MAXIMIZE_BOX)
        self.SetSize(self.ClientToWindowSize((960, 640)))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        
        self.config = WordPlateConfig()
        if self.config.Read("WordPlateConfig.ini") == False:
            self.config.ReadJson("WordPlateConfig.json")
        
        chioce_values = [14, 17, 20] if self.config.word_plate_player_count < 4 else [14, 17]
        if self.config.word_plate_everyone_count not in chioce_values:
            self.config.word_plate_everyone_count = chioce_values[0]        
        global NORMAL_WORD_PLATE_COUNT
        NORMAL_WORD_PLATE_COUNT = self.config.word_plate_everyone_count

        self.save_config_path = None
        
        self.canvas = DragCanvas(self)
        frame_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.canvas.SetSizer(frame_sizer)
        
        self.btn_setting = wx.Button(self.canvas, label=u"设置", size = (40, -1))
        self.btn_config_path = wx.Button(self.canvas, label=u"设置保存路径", size = (90, -1))
        self.btn_save = wx.Button(self.canvas, label=u"保存", size = (40, -1))
        settings_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        settings_sizer.Add(self.btn_setting, 0, wx.LEFT, 2)
        settings_sizer.AddStretchSpacer(1)
        settings_sizer.Add(self.btn_config_path, 0, wx.RIGHT, 2)
        settings_sizer.Add(self.btn_save, 0, wx.RIGHT, 2)
        frame_sizer.Add(settings_sizer, 1, wx.ALL|wx.EXPAND, 0)
        
        self.Bind(wx.EVT_CLOSE,  self.OnClose)
        self.Bind(wx.EVT_BUTTON, self.OnBtnSetting, self.btn_setting)
        self.Bind(wx.EVT_BUTTON, self.OnBtnConfigPath, self.btn_config_path)
        self.Bind(wx.EVT_BUTTON, self.OnBtnSave, self.btn_save)
        
    def __del__(self):
        
        self.config.Write("WordPlateConfig.ini")
        self.config.WriteJson("WordPlateConfig.json")
        print('save config to file')
        
    def OnClose(self, evt):
 
        self.canvas.SaveWordPlateViewToConfig()
        evt.Skip()
        

    def OnBtnSetting(self, evt):
        
        setting_dlg = WordPlateSettingDlg(self)
        setting_dlg.ShowModal()
        setting_dlg.Destroy()
        
        global NORMAL_WORD_PLATE_COUNT
        NORMAL_WORD_PLATE_COUNT = self.config.word_plate_everyone_count
    
        self.canvas.ResetWordPlateView()
        self.canvas.UpdateWordPlateView()
        
    def OnBtnConfigPath(self,  evt):
        
        wildcard = "config file format ini (WordPlateConfig.ini)|*.ini|"     \
                   "config file format json (WordPlateConfig.json)|*.json|" \
                   "All files (*.*)|*.*"        
        file_dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(),
                                  defaultFile="WordPlateConfig.ini", wildcard=wildcard, style=wx.SAVE)
        file_dlg.SetFilterIndex(0)
        if file_dlg.ShowModal() == wx.ID_OK:
            self.save_config_path = file_dlg.GetPath()
        
        
    def OnBtnSave(self, evt):
        
        if self.save_config_path != None:
            self.canvas.SaveWordPlateViewToConfig()
            if os.path.isdir(self.save_config_path):
                save_path =  os.path.join(self.save_config_path, "WordPlateConfig.ini")
                self.config.Write(save_path)
                save_path =  os.path.join(self.save_config_path, "WordPlateConfig.json")
                self.config.WriteJson(save_path)
            else:
                file_name = os.path.basename(self.save_config_path)
                ext_name =  os.path.splitext(file_name)[1]
                if ext_name.lower() == '.json':
                    self.config.WriteJson(self.save_config_path)
                else:
                    self.config.Write(self.save_config_path)
            
            wx.MessageBox(u"保存成功！", u"温馨提示", wx.OK, self)
        

class WordPlateApp(wx.App):  

    def OnInit(self):
        frame = WordPlateMainFrame()
        frame.Show(True)
        return True
    


def main():
    """software start runing """

    app = WordPlateApp()  
    app.MainLoop()

    return

    
if __name__ == "__main__":
    main()

 
