
import requests,json,os,time
import db

curdir=os.path.abspath(".")
logtxtdir=os.path.join(curdir,"logtxt")
if not os.path.exists(logtxtdir):
    os.mkdir(logtxtdir)


def getSpecialList(level1,key,signsafe,page):
    # proxies = { "http": "http://127.0.0.1:8888", "https": "https://127.0.0.1:8888", }  
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    url=f"https://api.eol.cn/web/api/?keyword=&level1={level1}&level2={key}&page={page}&size=100&sort=&uri=apidata/api/gkv3/special/lists&signsafe={signsafe}"
    postdata={"keyword":"","level1":f"{level1}","level2":f"{key}","page":page,"signsafe":f"{signsafe}","size":100,"sort":"","uri":"apidata/api/gkv3/special/lists"}
    #rsp=requests.post(url,json=postdata,verify=False)
    filename=os.path.join(logtxtdir,f"{key}_p{page}.txt")
    if not os.path.exists(filename):
        rsp=requests.post(url,data=json.dumps(postdata),headers=headers, verify=False,proxies=None)
        with open(filename,"w",encoding="utf-8") as file:
            file.write(rsp.text)
    
        jsondata=json.loads(rsp.text)
        datas=jsondata.get("data").get("item")
        for data in datas:
            db.insert(data)
        print(f"获取专业{key}_{page}完成")
        if jsondata.get("data").get("numFound")>page*30:
            getSpecialList(level1,key,signsafe,page+1)
            
    else:
        print(f"专业信息{key}已存在")
    
    

def getSpecialDetail(id):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    url=f"https://static-data.gaokao.cn/www/2.0/special/{id}/pc_special_detail.json"
    
    filename=os.path.join(logtxtdir,f"id_{id}.txt")
    if not os.path.exists(filename):
        rsp=requests.get(url,headers=headers, verify=False,proxies=None)
        with open(filename,"w",encoding="utf-8") as file:
            file.write(rsp.text)
    
        jsondata=json.loads(rsp.text)
        data=jsondata.get("data")
        item=[]
        impress=[]
        for dataitem in data.get("impress"):
            impress.append(dataitem.get("key_word"))
            #插入第一印象
            impressdata=[dataitem.get("id"),dataitem.get("key_word"),dataitem.get("special_id")]
            db.insertimpress(impressdata)
        
        

        jobrate=[]
        for dataitem in data.get("jobrate"):
            jobrate.append(f"{dataitem.get('year')}年:{dataitem.get('rate')}")
            #插入就业率
            jyldata=[dataitem.get("special_id"),dataitem.get("id"),dataitem.get("rate"),dataitem.get("year")]
            db.insertjyl(jyldata)

        hy=[]
        if data.get("jobdetail").get("1"):
            for dataitem in data.get("jobdetail").get("1"):
                hy.append(f"{dataitem.get('name')}:{dataitem.get('rate')}%")
                hydata=[dataitem.get("area"),dataitem.get("detail_job"),dataitem.get("detail_pos"),dataitem.get("id"),dataitem.get("name"),dataitem.get("rate"),dataitem.get("sort"),dataitem.get("special_id"),dataitem.get("type")]
                db.insertjyqk(hydata)
        
        dq=[]
        if data.get("jobdetail").get("2"):
            for dataitem in data.get("jobdetail").get("2"):
                dq.append(f"{dataitem.get('area')}:{dataitem.get('rate')}%")
                dqdata=[dataitem.get("area"),dataitem.get("detail_job"),dataitem.get("detail_pos"),dataitem.get("id"),dataitem.get("name"),dataitem.get("rate"),dataitem.get("sort"),dataitem.get("special_id"),dataitem.get("type")]
                db.insertjyqk(dqdata)

        fx=[]
        if data.get("jobdetail").get("3"):
            for dataitem in data.get("jobdetail").get("3"):
                fx.append(f"{dataitem.get('name')}:{dataitem.get('rate')}%")
                fxdata=[dataitem.get("area"),dataitem.get("detail_job"),dataitem.get("detail_pos"),dataitem.get("id"),dataitem.get("name"),dataitem.get("rate"),dataitem.get("sort"),dataitem.get("special_id"),dataitem.get("type")]
                db.insertjyqk(fxdata)

        item=[
            data.get("id"),
            data.get("code"),
            data.get("limit_year"),
            ','.join(impress),
            data.get("is_what"),
            ";".join(jobrate),
            data.get("course"),
            ";".join(hy),
            ";".join(dq),
            ";".join(fx),
            data.get("learn_what"),
            data.get("do_what")
        ]

        db.insertdetail(item)
        print(f"获取详情{id}完成")
    else:
        print(f"获取详情{id}已经存在")


# create table 专业信息
# (
# select sp.spcode as 专业代号, 
# sp.level2_name as 类型,
# sp.level3_name as 子类,
# sp.name as 专业 ,
# concat('是什么',Char(10),d.is_what,Char(10),'学什么',Char(10),d.learn_what,Char(10),'干什么',Char(10),d.do_what) as 专业简介,
# case when impress='' then '\\' else d.impress end as 专业关键词,
# case when impress='' then '\\' else d.course end as 开设课程,
# case when d.jobdetail_hy='' then 0 else 1 end as 是否有就业信息
# from speciallist sp
# left join detail d on d.special_id=sp.special_id
# )



# create table 就业情况(
# select sp.spcode as 专业代码, sp.name as 专业名称,
# case when ifnull(jy.detail_pos,'')='' then '\\' else concat(jy.detail_pos,":",rate,"%") end as 岗位类型,
# case when ifnull(jy.name,'')='' then '\\' else jy.name end as 所在行业,
# case when ifnull(jy.detail_job,'')='' then '\\' else jy.detail_job end  as 具体职位 

# from speciallist sp
# left join jyqk jy on sp.special_id=jy.special_id and type=3
# )


    
    

if __name__=="__main__":

    print("获取专业信息")
    # 本科
    getSpecialList(1,3,"bee4c188902c81c4b7da14fa1d8ef2be",1)
    getSpecialList(1,4,"93ca46a1d5a17522873a52833f3cdc6d",1)
    getSpecialList(1,5,"ea7a20f63acbb702d722009be4dcd399",1)
    getSpecialList(1,6,"033562c38babf68675311b163f695b82",1)
    getSpecialList(1,7,"7105fef8bbb35a04e3b3769cf03cad4c",1)
    getSpecialList(1,8,"23ba6b103cf5f619d9e3b9954761fced",1)
    getSpecialList(1,9,"92eef85732ee385481f6ad1a2913e8b5",1)
    getSpecialList(1,10,"9aec1762ea8590b32b28055a706e952b",1)
    getSpecialList(1,11,"a3591634d052e670649f0cbad1b3328a",1)
    getSpecialList(1,12,"44ca75c9ce08225c3d2716bdb0466792",1)
    getSpecialList(1,13,"f6571be27e8fd7d4beea95037ed39280",1)
    getSpecialList(1,14,"f73162150b664280420aa56ffcca48a0",1)

    # 专职
    getSpecialList(2,15,"8aceac23f66feccb0d85949a351c797d",1)
    getSpecialList(2,16,"7d3ace70d04ed8ac2df15dc9eaf1f588",1)
    getSpecialList(2,17,"5e1d3cf7a698c3c67b98650ae34fdfa3",1)
    getSpecialList(2,18,"55a796b4d76cd12f99ed2d055cbe310f",1)
    getSpecialList(2,19,"822147de1c3da22e09fb90b6852637ee",1)
    getSpecialList(2,20,"197c27acc00b71aa099727a4bdbd123b",1)
    getSpecialList(2,21,"5141d542479f75db9ade5fa9d6209cc5",1)
    getSpecialList(2,22,"ab7dec61b305f7c921028b4fc9873cf1",1)
    getSpecialList(2,23,"cb5a6f068fabb9d26e0b58fb5ba70710",1)
    getSpecialList(2,24,"4e9d92c4fd7ea2adabfd37939d99658c",1)
    getSpecialList(2,25,"c53a45fab0c14e7c31b68ebf982d48d1",1)
    getSpecialList(2,26,"ae957315717d843f38f9a09e935098c7",1)
    getSpecialList(2,27,"eed41bf0b8964e3b8cb7b095eaa40f79",1)
    getSpecialList(2,28,"94f06d64b6b6c1a28e8c36037e3ad886",1)
    getSpecialList(2,29,"cb6ae6f771978e773fe25e6eb88644ba",1)
    getSpecialList(2,30,"0ec4516466b5bf8efdb6e4ddb1210e16",1)
    getSpecialList(2,31,"5d4d6f433e53557084efa38d1e329e66",1)
    getSpecialList(2,32,"edea9fdc516fa321ed2cef60a5cfdaf7",1)
    getSpecialList(2,33,"65252fa87b9fe8de74c6c14df3705e92",1)

    # getSpecialList(15,"8aceac23f66feccb0d85949a351c797d",2)
    # getSpecialList(16,"7d3ace70d04ed8ac2df15dc9eaf1f588",2)
    # getSpecialList(17,"5e1d3cf7a698c3c67b98650ae34fdfa3",2)
    # getSpecialList(18,"55a796b4d76cd12f99ed2d055cbe310f",2)
    # getSpecialList(19,"822147de1c3da22e09fb90b6852637ee",2)
    # getSpecialList(20,"197c27acc00b71aa099727a4bdbd123b",2)
    # getSpecialList(21,"5141d542479f75db9ade5fa9d6209cc5",2)
    # getSpecialList(22,"ab7dec61b305f7c921028b4fc9873cf1",2)
    # getSpecialList(23,"cb5a6f068fabb9d26e0b58fb5ba70710",2)
    # getSpecialList(24,"4e9d92c4fd7ea2adabfd37939d99658c",2)
    # getSpecialList(25,"c53a45fab0c14e7c31b68ebf982d48d1",2)
    # getSpecialList(26,"ae957315717d843f38f9a09e935098c7",2)
    # getSpecialList(27,"eed41bf0b8964e3b8cb7b095eaa40f79",2)
    # getSpecialList(28,"94f06d64b6b6c1a28e8c36037e3ad886",2)
    # getSpecialList(29,"cb6ae6f771978e773fe25e6eb88644ba",2)
    # getSpecialList(30,"0ec4516466b5bf8efdb6e4ddb1210e16",2)
    # getSpecialList(30,"0ec4516466b5bf8efdb6e4ddb1210e16",2)
    # getSpecialList(31,"5d4d6f433e53557084efa38d1e329e66",2)
    # getSpecialList(32,"edea9fdc516fa321ed2cef60a5cfdaf7",2)
    # getSpecialList(33,"65252fa87b9fe8de74c6c14df3705e92",2)

    print("获取专业详情")
    ids=db.QuerySpid()
    for id in ids:
        getSpecialDetail(id[0])
        time.sleep(2)
        

    print("采集完成")
    


