-- ################
-- #    SCHEMA    #
-- ################

CREATE SCHEMA cad;

-- ################
-- #  SEQUENCES   #
-- ################

CREATE SEQUENCE cad.categoria_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.subcategoria_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  
  CREATE SEQUENCE cad.evento_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.evento_historico_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.status_evento_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.evento_observacao_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.viatura_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.instituicao_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.tipo_patrulha_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

-- ################
-- #    TABLES    #
-- ################

CREATE TABLE cad.tb_categoria_cat (
	id_categoria_cat integer NOT NULL DEFAULT nextval('cad.categoria_seq'::regclass),
	txt_categoria_cat varchar(50) NOT NULL,
	dat_inicio_cat timestamp without time zone NOT NULL,
	dat_fim_cat timestamp without time zone,
	CONSTRAINT categoria_pkey PRIMARY KEY (id_categoria_cat)
);

CREATE TABLE cad.tb_status_evento_sev (
	id_status_evento_sev integer NOT NULL DEFAULT nextval('cad.status_evento_seq'::regclass),
	txt_status_evento_sev varchar(50) NOT NULL,
	dat_inicio_sev timestamp without time zone NOT NULL,
	dat_fim_sev timestamp without time zone,
	CONSTRAINT status_evento_pkey PRIMARY KEY (id_status_evento_sev)
);

CREATE TABLE cad.tb_subcategoria_sub (
	id_subcategoria_sub integer NOT NULL DEFAULT nextval('cad.subcategoria_seq'::regclass),
  id_categoria_sub integer NOT NULL,
	txt_subcategoria_sub varchar(50) NOT NULL,
	dat_inicio_sub timestamp without time zone NOT NULL,
	dat_fim_sub timestamp without time zone,
	CONSTRAINT subcategoria_pkey PRIMARY KEY (id_subcategoria_sub)
);
ALTER TABLE cad.tb_subcategoria_sub ADD CONSTRAINT categoria_fkey FOREIGN KEY (id_categoria_sub) REFERENCES cad.tb_categoria_cat (id_categoria_cat);

CREATE TABLE cad.tb_evento_eve (
	id_evento_eve integer NOT NULL DEFAULT nextval('cad.evento_seq'::regclass),
  id_subcategoria_eve integer NOT NULL,
  id_usuario_eve integer NOT NULL,
  num_ocorrencia_eve varchar(15) NOT NULL,
	txt_problema_eve varchar(1000) NOT NULL,
  txt_endereco_eve varchar(1000) NOT NULL,
  txt_latitude_eve varchar(20) NOT NULL,
  txt_longitude_eve varchar(20) NOT NULL,
  img_file_eve bytea NOT NULL,
	dat_inicio_eve timestamp without time zone NOT null default now(),
	dat_fim_eve timestamp without time zone default null,
	CONSTRAINT evento_pkey PRIMARY KEY (id_evento_eve)
);
ALTER TABLE cad.tb_evento_eve ADD CONSTRAINT subcategoria_fkey FOREIGN KEY (id_subcategoria_eve) REFERENCES cad.tb_subcategoria_sub (id_subcategoria_sub);
ALTER TABLE cad.tb_evento_eve ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_eve) REFERENCES comum.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cad.tb_evento_historico_ehi (
	id_evento_historico_ehi integer NOT NULL DEFAULT nextval('cad.evento_historico_seq'::regclass),
  id_evento_ehi integer NOT NULL,
	id_status_evento_ehi integer NOT NULL,
  id_usuario_ehi integer NOT NULL,
	dat_inicio_ehi timestamp without time zone NOT null default now(),
	dat_fim_ehi timestamp without time zone default null,
	CONSTRAINT evento_historico_pkey PRIMARY KEY (id_evento_historico_ehi)
);
ALTER TABLE cad.tb_evento_historico_ehi ADD CONSTRAINT evento_fkey FOREIGN KEY (id_evento_ehi) REFERENCES cad.tb_evento_eve (id_evento_eve);
ALTER TABLE cad.tb_evento_historico_ehi ADD CONSTRAINT status_fkey FOREIGN KEY (id_status_evento_ehi) REFERENCES cad.tb_status_evento_sev (id_status_evento_sev);
ALTER TABLE cad.tb_evento_historico_ehi ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_ehi) REFERENCES comum.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cad.tb_evento_observacao_eob (
	id_evento_observacao_eob integer NOT NULL DEFAULT nextval('cad.evento_observacao_seq'::regclass),
  id_evento_historico_eob integer NOT NULL,
  id_usuario_eob integer NOT NULL,
	txt_evento_observacao_eob varchar(500) NOT NULL,
	dat_inicio_eob timestamp without time zone NOT NULL,
	dat_fim_eob timestamp without time zone,
	CONSTRAINT evento_observacao_pkey PRIMARY KEY (id_evento_observacao_eob)
);
ALTER TABLE cad.tb_evento_observacao_eob ADD CONSTRAINT evento_observacao_fkey FOREIGN KEY (id_evento_historico_eob) REFERENCES cad.tb_evento_historico_ehi (id_evento_historico_ehi);
ALTER TABLE cad.tb_evento_observacao_eob ADD CONSTRAINT usuario_observacao_fkey FOREIGN KEY (id_usuario_eob) REFERENCES comum.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cad.tb_instituicao_ins (
	id_instituicao_ins integer NOT NULL DEFAULT nextval('cad.instituicao_seq'::regclass),
	txt_instituicao_ins varchar(50) NOT NULL,
	dat_inicio_ins timestamp without time zone NOT NULL,
	dat_fim_ins timestamp without time zone,
	CONSTRAINT sinstituicao_pkey PRIMARY KEY (id_instituicao_ins)
);

CREATE TABLE cad.tb_tipo_patrulha_tpa (
	id_tipo_patrulha_tpa integer NOT NULL DEFAULT nextval('cad.tipo_patrulha_seq'::regclass),
	txt_tipo_patrulha_tpa varchar(50) NOT NULL,
	dat_inicio_tpa timestamp without time zone NOT NULL,
	dat_fim_tpa timestamp without time zone,
	CONSTRAINT tipo_patrulha_pkey PRIMARY KEY (id_tipo_patrulha_tpa)
);

CREATE TABLE cad.tb_viatura_via (
	id_viatura_via integer NOT NULL DEFAULT nextval('cad.viatura_seq'::regclass),
  id_instituicao_via integer NOT NULL,
  id_tipo_patrulha_via integer NOT NULL,
  txt_descricao_via varchar(100) NOT NULL,
	txt_codigo_via varchar(30) NOT NULL,
  txt_placa_via varchar(7) NOT NULL,
  dat_inicio_via timestamp without time zone NOT NULL,
	dat_fim_via timestamp without time zone,
	CONSTRAINT viatura_pkey PRIMARY KEY (id_viatura_via)
);
ALTER TABLE cad.tb_viatura_via ADD CONSTRAINT instituicao_fkey FOREIGN KEY (id_instituicao_via) REFERENCES cad.tb_instituicao_ins (id_instituicao_ins);
ALTER TABLE cad.tb_viatura_via ADD CONSTRAINT tipo_patrulha_fkey FOREIGN KEY (id_tipo_patrulha_via) REFERENCES cad.tb_tipo_patrulha_tpa (id_tipo_patrulha_tpa);


-- ####################################
-- #        INSERTS PARA TESTES       #
-- ####################################

INSERT INTO cad.tb_categoria_cat(txt_categoria_cat, dat_inicio_cat, dat_fim_cat)VALUES('Acidente', now(), null);
INSERT INTO cad.tb_categoria_cat(txt_categoria_cat, dat_inicio_cat, dat_fim_cat)VALUES('Assalto', now(), null);


INSERT INTO cad.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(1, 'Com vítimas fatais', now(), null);
INSERT INTO cad.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(1, 'Sem vítimas fatais', now(), null);

INSERT INTO cad.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(2, 'Com reféns', now(), null);
INSERT INTO cad.tb_subcategoria_sub(id_categoria_sub, txt_subcategoria_sub, dat_inicio_sub, dat_fim_sub)VALUES(2, 'Sem reféns', now(), null);

INSERT INTO cad.tb_status_evento_sev (txt_status_evento_sev, dat_inicio_sev, dat_fim_sev) VALUES('Aguardando Despacho', now(), null);
INSERT INTO cad.tb_status_evento_sev (txt_status_evento_sev, dat_inicio_sev, dat_fim_sev) VALUES('Em andamento', now(), null);
INSERT INTO cad.tb_status_evento_sev (txt_status_evento_sev, dat_inicio_sev, dat_fim_sev) VALUES('Finalizado', now(), null);

INSERT INTO cad.tb_instituicao_ins (txt_instituicao_ins, dat_inicio_ins, dat_fim_ins) VALUES('Trânsito', now(), null);
INSERT INTO cad.tb_instituicao_ins (txt_instituicao_ins, dat_inicio_ins, dat_fim_ins) VALUES('PM', now(), null);
INSERT INTO cad.tb_instituicao_ins (txt_instituicao_ins, dat_inicio_ins, dat_fim_ins) VALUES('CBM', now(), null);

INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Carro', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Moto', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Bicicleta', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Cavalo', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Andando', now(), null);