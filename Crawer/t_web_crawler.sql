drop table if exists t_web_crawler;

/*==============================================================*/
/* Table: t_web_crawler                                         */
/*==============================================================*/
create table t_web_crawler
(
   id                   varchar(32) not null comment '����',
   date                 varchar(8) comment '������',
   name                 varchar(100) comment '��Ӱ����',
   url                  varchar(100) comment '��ҳ��ַ',
   magnet               varchar(500) comment '��������',
   context              varchar(5000) comment '�������',
   create_time          datetime comment '����ʱ��',
   modify_time          datetime comment '�޸�ʱ��',
   is_delete            char(1) comment '�Ƿ�ɾ��(�߼�ɾ��) N����  Y����',
   primary key (id)
);

alter table t_web_crawler comment '������Ϣ��';
