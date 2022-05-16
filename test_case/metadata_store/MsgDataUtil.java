package com.tong.util.msgpack;

import com.tongtech.msgpackutil.MsgData;
import com.tongtech.msgpackutil.base.Base;
import com.tongtech.msgpackutil.base.ConfHead;
import com.tongtech.msgpackutil.conf.content.ConfTaskInfoSetReqContent;
import com.tongtech.msgpackutil.conf.model.ConfTaskInfoSetReqModel;
import com.tongtech.msgpackutil.metadata.content.CommonRdbSchemaReqContent;
import com.tongtech.msgpackutil.metadata.model.CommonRdbSchemaReqModel;
import lombok.extern.slf4j.Slf4j;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.*;

@Slf4j
public class MsgDataUtil {
    public static void main(String[] args) {
        try {
            //创建配置数据-任务信息测试数据
            CommonRdbSchemaReqModel<ConfHead, CommonRdbSchemaReqContent> configInfo = getConfInfo();

            //调用msgpack工具类打包
            byte[] serialize = MsgData.serialize(configInfo);
            System.out.println("配置数据-任务信息 序列化byte[]数据="+ Arrays.toString(serialize));


            //调用msgpack工具类解包
            MsgData msgdata = MsgData.deserialize(serialize);

            //调用工厂类(一个产品维护一份) 根据base中的大类可以确定具体head，根据base中的大类+小类可以确定具体的content 用于类型强转获取具体head content值
            //数据大类 4：配置 SET；5:配置 GET；6:配置 DEL
            int dataType = msgdata.base.getDataType();
            //数据小类 0x01、0x81、0x02、0x82、0x03、0x83...0x12、0x92
            int subDataType = msgdata.base.getSubDataType();
            String contentType = String.valueOf(dataType)+"&"+String.valueOf(subDataType);

            switch(contentType){
                //配置数据-任务信息
                case "8&17":
                    //配置数据-任务信息 set请求
                    //强转为具体的content
                    CommonRdbSchemaReqContent content = (CommonRdbSchemaReqContent) msgdata.content;
                    List<Map<String, String>> listMap = content.getList();
                    for(int i=0;i<listMap.size();i++) {
                        Set<String> keys = listMap.get(i).keySet();
                        for (String key : keys) {
                            System.out.println("(" + key + ", " + listMap.get(i).get(key) + ")");
                        }
                    }
                case "4&131":
                    //配置数据-任务信息 set响应
                case "5&3":
                    //配置数据-任务信息 get请求
                case "5&131":
                    //配置数据-任务信息 get响应
                case "6&3":
                    //配置数据-任务信息 del请求
                case "6&131":
                    //配置数据-任务信息 del响应
            }
            writeFile("E:/","test.msg",serialize);
        } catch (Exception e) {
            e.printStackTrace();
        }


    }

    /**
     * 组装配置代理&服务中心 测试数据
     * 配置数据-任务信息
     * @return
     */
    public static CommonRdbSchemaReqModel getConfInfo() throws Exception{
        CommonRdbSchemaReqModel configInfo = new CommonRdbSchemaReqModel();
        Base pb = new Base();
        pb.setVersion(1);
        pb.setDataType(8);
        pb.setProduct(242);
        pb.setSubDataType(0x11);
        pb.setTimestamp((long)12345678);
        pb.setNodeId(13);
        pb.setClusterid((long)7);
        configInfo.base = pb;

        ConfHead ch = new ConfHead();
        ch.setWorkNum("opid123");
        ch.setProcessid("12");
        ch.setStatus(7);
        ch.setOutTime(60);
        configInfo.head = ch;

        CommonRdbSchemaReqContent content = new CommonRdbSchemaReqContent();
        List<Map<String,String>> listMap = new ArrayList<>();
        Map<String, String> map = new HashMap<>();
        map.put("dbtype","18");
        map.put("driver","com.mysql.cj.jdbc.Driver");
        map.put("url","jdbc:mysql://10.10.64.23/sql_test?characterEncoding=utf8&useSSL=false&serverTimezone=UTC&rewriteBatchedStatements=true");
        map.put("user","root");
        map.put("passwd","Tong.1818");
        listMap.add(map);
        content.setList(listMap);
        configInfo.content = content;

        return configInfo;
    }

    public static void writeFile(String path, String fileName, byte[] content)
            throws IOException {
        try {
            File f = new File(path);
            if (!f.exists()) {
                f.mkdirs();
            }
            FileOutputStream fos = new FileOutputStream(path + fileName);
            fos.write(content);
            fos.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
