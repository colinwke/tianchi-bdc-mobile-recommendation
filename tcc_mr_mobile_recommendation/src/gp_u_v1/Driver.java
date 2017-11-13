package gp_u_v1;

import com.aliyun.odps.OdpsException;
import com.aliyun.odps.data.TableInfo;
import com.aliyun.odps.mapred.JobClient;
import com.aliyun.odps.mapred.RunningJob;
import com.aliyun.odps.mapred.conf.JobConf;
import com.aliyun.odps.mapred.utils.InputUtils;
import com.aliyun.odps.mapred.utils.OutputUtils;
import com.aliyun.odps.mapred.utils.SchemaUtils;

public class Driver {

    public static void main(String[] args) throws OdpsException {

        JobConf job = new JobConf();

        // TODO: specify map output types
        job.setMapOutputKeySchema(SchemaUtils.fromString("user_id:STRING"));
        // delete user_geo
        job.setMapOutputValueSchema(SchemaUtils.fromString("behavior_type:BIGINT,date:BIGINT")); 

        // TODO: specify input and output tables
        InputUtils.addTable(TableInfo.builder().tableName("in_interaction_subitem_drop1112_reshape_date").build(), job);
        OutputUtils.addTable(TableInfo.builder().tableName("out_gp_u_v1").build(), job);

        // TODO: specify a mapper
        job.setMapperClass(gp_u_v1.Mapper.class);
        // TODO: specify a reducer
        job.setReducerClass(gp_u_v1.Reducer.class);

        RunningJob rj = JobClient.runJob(job);
        
        rj.waitForCompletion();

    }

}