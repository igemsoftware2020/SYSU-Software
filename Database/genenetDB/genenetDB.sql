USE genenetDB;

SET SESSION SQL_MODE=ANSI_QUOTES;

-- DROP TABLE IF EXISTS "BindingSiteSet";  
DROP TABLE IF EXISTS "PromoterSet";
-- DROP TABLE IF EXISTS "TFSet";

CREATE TABLE IF NOT EXISTS "BindingSiteSet"(
	id INTEGER NOT NULL AUTO_INCREMENT,
	TF_identifier VARCHAR(50) NOT NULL,
    TF_name	VARCHAR(50),
    Confornation_name TEXT,
    TF_bs_identifier VARCHAR(50),
    TF_bs_left_end_pos VARCHAR(10),
    TF_bs_right_end_pos VARCHAR(10),
    DNA_strand VARCHAR(10),
    TF_gene_interaction_identifier VARCHAR(50),
    Tran_unit_id VARCHAR(50),
    Tran_unit_name TEXT,
    Gene_expr_effect VARCHAR(2),
    Promoter_name VARCHAR(50),
    TF_bs_center_pos VARCHAR(10),
    TF_bs_sequence TEXT,
    Dist_to_1st_gene VARCHAR(10),
    Evidence TEXT,
    Evidence_level VARCHAR(10),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS "PromoterSet"(
	id INTEGER NOT NULL AUTO_INCREMENT NOT NULL,
    Promoter_identifier VARCHAR(50),
    Promoter_name TEXT,
    DNA_strand VARCHAR(10),
    Genome_map_pos VARCHAR(10),
    Sigma_factor VARCHAR(50),
    Promoter_sequence TEXT,
	Evidence TEXT,
    Evidence_level VARCHAR(10),
    Count_pos INTEGER,
    Count_neg INTEGER,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS "TFSet" (
	id INTEGER NOT NULL AUTO_INCREMENT,
    TF_identifier VARCHAR(50) NOT NULL,
    TF_name VARCHAR(50),
    Gene_coding VARCHAR(50),
    TF_active_conf TEXT,
    TF_inactive_conf TEXT,
    Evidence TEXT,
    PMID TEXT,
    Evidence_level VARCHAR(10),
    PRIMARY KEY(id)
);

use genenetDB;

drop table if exists genenet_BindingSite;
drop table if exists genenet_Promoter;
drop table if exists genenet_TF_Gene;
drop table if exists genenet_Gene;
drop table if exists genenet_TF;

create table if not exists genenet_TF(
	persistentIdentity varchar(100),
    TF_name			   varchar(100),
    sequence_len	   integer, -- = max(corresponding gene.sequence_len)
    cite			   integer,
    PMID			   text,
    primary key(persistentIdentity)
);

create table if not exists genenet_Gene(
	persistentIdentity varchar(100),
    gene_name 		   varchar(100),
    sequence		   text,
    sequence_len	   integer,
 --    TF_name			   varchar(100), -- this gene corresponds to a TF
    primary key(persistentIdentity)
);

create table if not exists genenet_TF_Gene(
	TF_name			   varchar(100),
    gene_name		   varchar(100),
    primary key(TF_name, gene_name)
);

create table if not exists genenet_Promoter(
	persistentIdentity varchar(100),
    pro_name	  	   varchar(100),
    sequence		   text,
    sequence_len	   integer, 
    cite			   integer, 
    num_pos_TFs		   integer,
    num_neg_TFs		   integer,
    pos_TFs			   text,
    neg_TFs			   text,
    primary key(persistentIdentity)
);

create table if not exists genenet_BindingSite(
	TF_id			  varchar(100),
    TF_name			  varchar(100),
    pro_name		  varchar(100),
    effect			  varchar(1), -- -1 or +1
    TF_bs_sequence	  varchar(200),
    origin_BindingSiteSet_id integer,
    primary key(origin_BindingSiteSet_id),
    foreign key(TF_id) references genenet_TF(persistentIdentity)
);

insert into genenet_TF(persistentIdentity, TF_name, sequence_len, PMID)
select a.TF_identifier, a.TF_name, a.TF_sequence_len, a.PMID
from TFSet as a;

set SQL_SAFE_UPDATES = 1;
update genenet_TF as a set cite = (select distinct TF_cite_sum from BindingSiteSet as b where a.persistentIdentity = b.TF_identifier);

insert into	genenet_Gene(persistentIdentity, gene_name, sequence, sequence_len)
select distinct gene_id, gene_name, gene_sequence, gene_posright - gene_posleft
from GENE;

insert into genenet_TF_Gene
select a.TF_name, b.gene_name
from TFSet as a, genenet_Gene as b
where a.Gene_coding like concat(concat('%', b.gene_name), '%');

insert into genenet_Promoter
select promoter_id, promoter_name, promoter_sequence, length(promoter_sequence), cite_sum, Count_pos, Count_neg
from _PROMOTER;

insert into genenet_BindingSite
select TF_identifier, TF_name, Promoter_name, Gene_expr_effect, TF_bs_sequence, id
from BindingSiteSet;

update genenet_Promoter as a set pos_TFs = (select count(distinct TF_id) from genenet_BindingSite as b where a.pro_name = b.pro_name and b.effect = '+');
update genenet_Promoter as a set neg_TFs = (select count(distinct TF_id) from genenet_BindingSite as b where a.pro_name = b.pro_name and b.effect = '-');

create index index_Binding on genenet_BindingSite (TF_name, pro_name, effect);

create index index_Binding_1 on genenet_BindingSite (TF_name, pro_name);
-- alter table genenet_Promoter rename column pos_TFs to num_pos_TFs;
-- alter table genenet_Promoter rename column neg_TFs to num_neg_TFs;
-- alter table genenet_Promoter add column pos_TFs text;
-- alter table genenet_Promoter add column neg_TFs text;

-- update genenet_Promoter as a set pos_TFs = 
-- (select concat_ws(',', distinct TF_id) from genenet_BindingSite as b where a.pro_name = b.pro_name and b.effect = '+');

