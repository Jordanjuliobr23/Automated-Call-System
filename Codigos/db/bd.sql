-- ============================================================
-- TABELA: Professor
-- ============================================================
CREATE TABLE professor (
    idProfessor      SERIAL PRIMARY KEY,
    matricula        VARCHAR(20) UNIQUE NOT NULL,
    nome             VARCHAR(150) NOT NULL,
    senha_hash       TEXT NOT NULL
);

-- ============================================================
-- TABELA: Disciplina
-- ============================================================
CREATE TABLE disciplina (
    idDisciplina     SERIAL PRIMARY KEY,
    nome             VARCHAR(150) NOT NULL,
    sigla            VARCHAR(20) NOT NULL,
    curso            VARCHAR(150) NOT NULL
);

-- ============================================================
-- TABELA: Diario
-- ============================================================
CREATE TABLE diario (
    idDiario         SERIAL PRIMARY KEY,
    turno            VARCHAR(20) NOT NULL,
    idProfessor      INT NOT NULL REFERENCES professor(idProfessor),
    idDisciplina     INT NOT NULL REFERENCES disciplina(idDisciplina)
);

-- ============================================================
-- TABELA: Horario
-- ============================================================
CREATE TABLE horario (
    idHorario        SERIAL PRIMARY KEY,
    horaInicio       TIME NOT NULL,
    horaFim          TIME NOT NULL,
    tolerancia       INT NOT NULL  -- minutos após o início
);

-- ============================================================
-- TABELA: Aula
-- ============================================================
CREATE TABLE aula (
    idAula           SERIAL PRIMARY KEY,
    data             DATE NOT NULL,
    conteudo         TEXT,
    numAula          INT NOT NULL,           -- quantidade de períodos
    idDiario         INT NOT NULL REFERENCES diario(idDiario),
    idHorario        INT NOT NULL REFERENCES horario(idHorario)
);

-- ============================================================
-- TABELA: Aluno
-- ============================================================
CREATE TABLE aluno (
    idAluno          SERIAL PRIMARY KEY,
    matricula        VARCHAR(20) UNIQUE NOT NULL,
    nome             VARCHAR(150) NOT NULL
);

-- ============================================================
-- TABELA: Chave (QR Code)
-- ============================================================
CREATE TABLE chave (
    idChave          SERIAL PRIMARY KEY,
    codigo           VARCHAR(255) NOT NULL UNIQUE,
    status           VARCHAR(30) NOT NULL,
    criadoEm         TIMESTAMP NOT NULL DEFAULT NOW(),
    usadoEm          TIMESTAMP,
    idAluno          INT NOT NULL REFERENCES aluno(idAluno),
    idAula           INT NOT NULL REFERENCES aula(idAula)
);

-- ============================================================
-- TABELA: Chamada
-- ============================================================
CREATE TABLE chamada (
    idChamada        SERIAL PRIMARY KEY,
    horaEntrada      TIMESTAMP NOT NULL,
    horaSaida        TIMESTAMP,              -- pode ser preenchido depois
    presencas        INT,                    -- minutos presentes (opcional)
    idAluno          INT NOT NULL REFERENCES aluno(idAluno),
    idAula           INT NOT NULL REFERENCES aula(idAula),
    idHorario        INT NOT NULL REFERENCES horario(idHorario),
    idChave          INT NOT NULL REFERENCES chave(idChave)
);

-- ============================================================
-- ÍNDICES IMPORTANTES PARA PERFORMANCE
-- ============================================================

-- busca de presenças por aluno e aula
CREATE INDEX idx_chamada_aluno ON chamada(idAluno);
CREATE INDEX idx_chamada_aula  ON chamada(idAula);

-- validação de chave (QR)
CREATE INDEX idx_chave_codigo  ON chave(codigo);

-- listagem de aulas no diário
CREATE INDEX idx_aula_diario   ON aula(idDiario);

-- listagem de chaves por aula
CREATE INDEX idx_chave_aula    ON chave(idAula);