-- ################
-- #    SCHEMA    #
-- ################

CREATE SCHEMA cad;

-- ################
-- #  SEQUENCES   #
-- ################

CREATE SEQUENCE cad.tipo_ocorrencia_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.subtipo_ocorrencia_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  
  CREATE SEQUENCE cad.ocorrencia_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.ocorrencia_historico_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.status_ocorrencia_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;

  CREATE SEQUENCE cad.ocorrencia_observacao_seq
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

  CREATE SEQUENCE cad.interessado_seq
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

CREATE TABLE cad.tb_tipo_ocorrencia_toc (
	id_tipo_ocorrencia_toc integer NOT NULL DEFAULT nextval('cad.tipo_ocorrencia_seq'::regclass),
	txt_tipo_ocorrencia_toc varchar(50) NOT NULL,
	dat_inicio_toc timestamp without time zone NOT NULL,
	dat_fim_toc timestamp without time zone,
	CONSTRAINT tipo_ocorrencia_pkey PRIMARY KEY (id_tipo_ocorrencia_toc)
);

CREATE TABLE cad.tb_subtipo_ocorrencia_soc (
	id_subtipo_ocorrencia_soc integer NOT NULL DEFAULT nextval('cad.subtipo_ocorrencia_seq'::regclass),
  id_tipo_ocorrencia_soc integer NOT NULL,
	txt_subtipo_ocorrencia_soc varchar(50) NOT NULL,
	dat_inicio_soc timestamp without time zone NOT NULL,
	dat_fim_soc timestamp without time zone,
	CONSTRAINT subtipo_ocorrencia_pkey PRIMARY KEY (id_subtipo_ocorrencia_soc)
);
ALTER TABLE cad.tb_subtipo_ocorrencia_soc ADD CONSTRAINT tipo_ocorrencia_fkey FOREIGN KEY (id_tipo_ocorrencia_soc) REFERENCES cad.tb_tipo_ocorrencia_toc (id_tipo_ocorrencia_toc);

CREATE TABLE cad.tb_status_ocorrencia_sto(
	id_status_ocorrencia_sto integer NOT NULL DEFAULT nextval('cad.status_ocorrencia_seq'::regclass),
	txt_status_ocorrencia_sto varchar(50) NOT NULL,
	dat_inicio_sto timestamp without time zone NOT NULL,
	dat_fim_sto timestamp without time zone,
	CONSTRAINT status_ocorrencia_pkey PRIMARY KEY (id_status_ocorrencia_sto)
);

CREATE TABLE cad.tb_ocorrencia_oco (
	id_ocorrencia_oco integer NOT NULL DEFAULT nextval('cad.ocorrencia_seq'::regclass),
  id_subtipo_ocorrencia_oco integer NOT NULL,
  id_usuario_oco integer NOT NULL,
  num_ocorrencia_oco varchar(15) NOT NULL,
	txt_problema_oco varchar(1000) NOT NULL,
  txt_endereco_oco varchar(1000) NOT NULL,
  txt_latitude_oco varchar(20) NOT NULL,
  txt_longitude_oco varchar(20) NOT NULL,
	dat_inicio_oco timestamp without time zone NOT null default now(),
	dat_fim_oco timestamp without time zone default null,
	CONSTRAINT ocorrencia_pkey PRIMARY KEY (id_ocorrencia_oco)
);
ALTER TABLE cad.tb_ocorrencia_oco ADD CONSTRAINT subtipo_ocorrencia_fkey FOREIGN KEY (id_subtipo_ocorrencia_oco) REFERENCES cad.tb_subtipo_ocorrencia_soc (id_subtipo_ocorrencia_soc);
ALTER TABLE cad.tb_ocorrencia_oco ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_oco) REFERENCES comum.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cad.tb_ocorrencia_historico_ohi (
	id_ocorrencia_historico_ohi integer NOT NULL DEFAULT nextval('cad.ocorrencia_historico_seq'::regclass),
  id_ocorrencia_ohi integer NOT NULL,
	id_status_ocorrencia_ohi integer NOT NULL,
  id_usuario_ohi integer NOT NULL,
	dat_inicio_ohi timestamp without time zone NOT null default now(),
	dat_fim_ohi timestamp without time zone default null,
	CONSTRAINT ocorrencia_historico_pkey PRIMARY KEY (id_ocorrencia_historico_ohi)
);
ALTER TABLE cad.tb_ocorrencia_historico_ohi ADD CONSTRAINT ocorrencia_fkey FOREIGN KEY (id_ocorrencia_ohi) REFERENCES cad.tb_ocorrencia_oco (id_ocorrencia_oco);
ALTER TABLE cad.tb_ocorrencia_historico_ohi ADD CONSTRAINT status_fkey FOREIGN KEY (id_status_ocorrencia_ohi) REFERENCES cad.tb_status_ocorrencia_sto (id_status_ocorrencia_sto);
ALTER TABLE cad.tb_ocorrencia_historico_ohi ADD CONSTRAINT usuario_fkey FOREIGN KEY (id_usuario_ohi) REFERENCES comum.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cad.tb_ocorrencia_observacao_oob (
	id_ocorrencia_observacao_oob integer NOT NULL DEFAULT nextval('cad.ocorrencia_observacao_seq'::regclass),
  id_ocorrencia_historico_oob integer NOT NULL,
  id_usuario_oob integer NOT NULL,
	txt_ocorrencia_observacao_oob varchar(500) NOT NULL,
	dat_inicio_oob timestamp without time zone NOT NULL,
	dat_fim_oob timestamp without time zone,
	CONSTRAINT ocorrencia_observacao_pkey PRIMARY KEY (id_ocorrencia_observacao_oob)
);
ALTER TABLE cad.tb_ocorrencia_observacao_oob ADD CONSTRAINT ocorrencia_observacao_fkey FOREIGN KEY (id_ocorrencia_historico_oob) REFERENCES cad.tb_ocorrencia_historico_ohi (id_ocorrencia_historico_ohi);
ALTER TABLE cad.tb_ocorrencia_observacao_oob ADD CONSTRAINT usuario_observacao_fkey FOREIGN KEY (id_usuario_oob) REFERENCES comum.tb_usuario_usu (id_usuario_usu);

CREATE TABLE cad.tb_instituicao_ins (
	id_instituicao_ins integer NOT NULL DEFAULT nextval('cad.instituicao_seq'::regclass),
	txt_instituicao_ins varchar(50) NOT NULL,
  txt_sigla_ins varchar(10) NOT NULL,
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

CREATE TABLE cad.tb_interessado_int (
	id_interessado_int integer NOT NULL DEFAULT nextval('cad.interessado_seq'::regclass),
  id_ocorrencia_int integer NOT NULL,
  txt_interessado_int varchar(100) NOT NULL,
	txt_cpf_int varchar(11),
  txt_telefone_int varchar(11) NOT NULL,
	CONSTRAINT interessado_pkey PRIMARY KEY (id_interessado_int)
);
ALTER TABLE cad.tb_interessado_int ADD CONSTRAINT ocorrencia_fkey FOREIGN KEY (id_ocorrencia_int) REFERENCES cad.tb_ocorrencia_oco (id_ocorrencia_oco);

-- ####################################
-- #        INSERTS PARA TESTES       #
-- ####################################

INSERT INTO cad.tb_tipo_ocorrencia_toc(txt_tipo_ocorrencia_toc, dat_inicio_toc, dat_fim_toc)VALUES('Acidente', now(), null);
INSERT INTO cad.tb_tipo_ocorrencia_toc(txt_tipo_ocorrencia_toc, dat_inicio_toc, dat_fim_toc)VALUES('Assalto', now(), null);


INSERT INTO cad.tb_subtipo_ocorrencia_soc(id_tipo_ocorrencia_soc, txt_subtipo_ocorrencia_soc, dat_inicio_soc, dat_fim_soc)VALUES(1, 'Com vítimas fatais', now(), null);
INSERT INTO cad.tb_subtipo_ocorrencia_soc(id_tipo_ocorrencia_soc, txt_subtipo_ocorrencia_soc, dat_inicio_soc, dat_fim_soc)VALUES(1, 'Sem vítimas fatais', now(), null);
INSERT INTO cad.tb_subtipo_ocorrencia_soc(id_tipo_ocorrencia_soc, txt_subtipo_ocorrencia_soc, dat_inicio_soc, dat_fim_soc)VALUES(2, 'Com reféns', now(), null);
INSERT INTO cad.tb_subtipo_ocorrencia_soc(id_tipo_ocorrencia_soc, txt_subtipo_ocorrencia_soc, dat_inicio_soc, dat_fim_soc)VALUES(2, 'Sem reféns', now(), null);

INSERT INTO cad.tb_status_ocorrencia_sto (txt_status_ocorrencia_sto, dat_inicio_sto, dat_fim_sto) VALUES('Aguardando Despacho', now(), null);
INSERT INTO cad.tb_status_ocorrencia_sto (txt_status_ocorrencia_sto, dat_inicio_sto, dat_fim_sto) VALUES('Em andamento', now(), null);
INSERT INTO cad.tb_status_ocorrencia_sto (txt_status_ocorrencia_sto, dat_inicio_sto, dat_fim_sto) VALUES('Finalizado', now(), null);

INSERT INTO cad.tb_instituicao_ins (txt_instituicao_ins, txt_sigla_ins, dat_inicio_ins, dat_fim_ins) VALUES('Trânsito', 'AMC', now(), null);
INSERT INTO cad.tb_instituicao_ins (txt_instituicao_ins, txt_sigla_ins, dat_inicio_ins, dat_fim_ins) VALUES('Polícia Militar', 'PM', now(), null);
INSERT INTO cad.tb_instituicao_ins (txt_instituicao_ins, txt_sigla_ins, dat_inicio_ins, dat_fim_ins) VALUES('Corpo de Bombeiros Militar', 'CBM', now(), null);

INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Carro', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Moto', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Bicicleta', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Cavalo', now(), null);
INSERT INTO cad.tb_tipo_patrulha_tpa (txt_tipo_patrulha_tpa, dat_inicio_tpa, dat_fim_tpa) VALUES('Andando', now(), null);