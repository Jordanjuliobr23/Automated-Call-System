create schema sistema_chamada;

--Tabela Professor
CREATE TABLE sistema_chamada.professor (
    matriculaProfessor VARCHAR(14) UNIQUE NOT NULL PRIMARY KEY,
    nomeProfessor VARCHAR(150) NOT NULL,
    senhaProfessor VARCHAR(200) NOT NULL    
);

--Tabela disciplina
CREATE TABLE sistema_chamada.disciplina (
    idDisciplina SERIAL PRIMARY KEY,
    nomeDisciplina VARCHAR(150) NOT NULL,
    siglaDisciplina VARCHAR(20) NOT NULL,
    curso VARCHAR(150) NOT NULL
);

--Tabela horário
CREATE TABLE sistema_chamada.horario (
    idHorario SERIAL PRIMARY KEY,
    horaInicio TIME NOT NULL,
    horaFim TIME NOT NULL,
    tolerancia TIME NOT NULL 
);

-- Tabelas que referenciam professor/disciplina/horario
CREATE TABLE sistema_chamada.diario (
    idDiario SERIAL PRIMARY KEY,
    turno VARCHAR(30) NOT NULL,
    disciplina INT NOT NULL REFERENCES sistema_chamada.disciplina(idDisciplina) ON DELETE CASCADE,
    professor VARCHAR(14) NOT NULL REFERENCES sistema_chamada.professor(matriculaProfessor)
);

--Tabela aula
CREATE TABLE sistema_chamada.aula (
    idAula SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    numAula INT NOT NULL,
    conteudo TEXT,
    diario INT NOT NULL REFERENCES sistema_chamada.diario(idDiario) ON DELETE CASCADE,
    horario INT NOT NULL REFERENCES sistema_chamada.horario(idHorario)
);

--Tabela Aluno 
CREATE TABLE sistema_chamada.aluno (
    matriculaAluno VARCHAR(14) UNIQUE NOT NULL PRIMARY KEY,
    nomeAluno VARCHAR(150) NOT NULL
);

--Tabela Chave 
CREATE TABLE sistema_chamada.chave (
    codigo VARCHAR(50) UNIQUE NOT NULL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    criadoEm TIMESTAMP DEFAULT now(),
    usadoEm TIMESTAMP,
    aluno VARCHAR(20) REFERENCES sistema_chamada.aluno(matriculaAluno) ON DELETE SET NULL,
    aula INT REFERENCES sistema_chamada.aula(idAula) ON DELETE SET NULL
);

--Tabela Chamada (registro de presença)
CREATE TABLE sistema_chamada.chamada (
    idChamada SERIAL PRIMARY KEY,
    horaEntrada TIMESTAMP,
    horaSaida TIMESTAMP,
    presencas INT,

    aula INT NOT NULL REFERENCES sistema_chamada.aula(idAula) ON DELETE CASCADE,
    horario INT REFERENCES sistema_chamada.horario(idHorario) ,  -- pode ser nulo se não desejar vincular
    chave VARCHAR(50) REFERENCES sistema_chamada.chave(codigo) ON DELETE SET NULL,
    aluno VARCHAR(20) NOT NULL REFERENCES sistema_chamada.aluno(matriculaAluno)
);














