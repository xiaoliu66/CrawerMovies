drop table if exists t_web_crawler;

/*==============================================================*/
/* Table: t_web_crawler                                         */
/*==============================================================*/
create table t_web_crawler
(
   id                   varchar(32) not null comment '主键',
   date                 varchar(8) comment '短日期',
   name                 varchar(100) comment '电影名称',
   url                  varchar(100) comment '网页地址',
   magnet               varchar(500) comment '磁力链接',
   context              varchar(5000) comment '简介内容',
   create_time          datetime comment '创建时间',
   modify_time          datetime comment '修改时间',
   is_delete            char(1) comment '是否删除(逻辑删除) N：否  Y：是',
   primary key (id)
);

alter table t_web_crawler comment '爬虫信息表';
