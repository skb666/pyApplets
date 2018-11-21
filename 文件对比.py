from funct import *

def jc(*PF):
    for pf in PF:
        g_zd=get_Newzd('%s:\\'%pf)
        bz_1=bz_2=bz_3=False
        try:
            with open('list_%s.json'%pf) as f_obj:
                y_zd=json.load(f_obj)
        except FileNotFoundError:
            with open('list_%s.json'%pf,'w') as f_obj:
                json.dump(g_zd,f_obj)
            y_zd={}
        if not y_zd:
            with open('change_%s.txt'%pf,'w') as f_obj:
                f_obj.write('这是第一次运行，下次运行将自动检查文件变化！')
        else:
            with open('change_%s.txt'%pf,'w') as f_obj:
                f_obj.write('')
            c_zd={'new':{},'del':{},'non':{}}
            for wjj in g_zd.keys():
                if wjj not in y_zd.keys():
                    c_zd['new'][wjj]=g_zd[wjj]
                else:
                    c_zd['non'][wjj]={'new':[],'del':[]}
            for wjj in y_zd.keys():
                if wjj not in g_zd.keys():
                    c_zd['del'][wjj]=y_zd[wjj]
            for wjj in c_zd['non'].keys():
                for wj in g_zd[wjj]:
                    if wj not in y_zd[wjj]:
                        c_zd['non'][wjj]['new'].append(wj)
                for wj in y_zd[wjj]:
                    if wj not in g_zd[wjj]:
                        c_zd['non'][wjj]['del'].append(wj)
            with open('list_%s.json'%pf,'w') as f_obj:
                json.dump(g_zd,f_obj)
            if c_zd['new']:
                bz_1=True
                for wjj in c_zd['new'].keys():
                    with open('change_%s.txt'%pf,'a') as f_obj:
                        f_obj.write('******************************************************************************************************************************************************\n'+wjj+'\n')
                    for wj in c_zd['new'][wjj]:
                        with open('change_%s.txt'%pf,'a') as f_obj:
                            f_obj.write('  (new) ├'+wj.replace(u'\xa0', u' ')+' --(更改:'+get_FileModifyTime(wjj+wj)+'|访问:'+get_FileAccessTime(wjj+wj)+'|创建:'+get_FileCreateTime(wjj+wj)+')\n')
            if c_zd['del']:
                bz_2=True
                for wjj in c_zd['del'].keys():
                    with open('change_%s.txt'%pf,'a') as f_obj:
                        f_obj.write('******************************************************************************************************************************************************\n'+wjj+'\n')
                    for wj in c_zd['del'][wjj]:
                        with open('change_%s.txt'%pf,'a') as f_obj:
                            f_obj.write('  (del) ├'+wj.replace(u'\xa0', u' ')+'\n')
            for wjj in c_zd['non'].keys():
                if c_zd['non'][wjj]['new'] or c_zd['non'][wjj]['del']:
                    bz_3=True
                    break
            if bz_3:
                for wjj in c_zd['non'].keys():
                    if c_zd['non'][wjj]['new'] or c_zd['non'][wjj]['del']:
                        with open('change_%s.txt'%pf,'a') as f_obj:
                            f_obj.write('******************************************************************************************************************************************************\n'+wjj+'\n')
                        if c_zd['non'][wjj]['new']:
                            for wj in c_zd['non'][wjj]['new']:
                                with open('change_%s.txt'%pf,'a') as f_obj:
                                    f_obj.write('  (new) ├'+wj.replace(u'\xa0', u' ')+' --(更改:'+get_FileModifyTime(wjj+wj)+'|访问:'+get_FileAccessTime(wjj+wj)+'|创建:'+get_FileCreateTime(wjj+wj)+')\n')
                        if c_zd['non'][wjj]['del']:
                            for wj in c_zd['non'][wjj]['del']:
                                with open('change_%s.txt'%pf,'a') as f_obj:
                                    f_obj.write('  (del) ├'+wj.replace(u'\xa0', u' ')+'\n')
            if not bz_1 and not bz_2 and not bz_3:
                with open('change_%s.txt'%pf,'a') as f_obj:
                    f_obj.write('该路径下文件无变动！')

if __name__=='__main__':
    jc('c','d')
    root = Tk() # 初始化Tk()
    root.title('提示')    # 设置窗口标题
    root.geometry('+560+300')    # 设置窗口大小 注意：是x 不是*
    root.resizable(width=False, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
    l = Label(root, text="对比完成！", bg="royalblue", font=("Arial",10), width=20, height=3)
    l.pack(side=LEFT)   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
    root.mainloop() # 进入消息循环