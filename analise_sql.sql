

SELECT COUNT(id_chamado) AS total_chamados # Resposta 1
FROM `datario.adm_central_atendimento_1746.chamado` 
WHERE DATE(data_inicio) = "2023-04-01";

SELECT tipo, COUNT(id_chamado) AS total_reclamacoes # Resposta 2
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = "2023-04-01"
GROUP BY tipo
ORDER BY total_reclamacoes DESC
LIMIT 1;



SELECT b.nome AS nome_bairro, b.subprefeitura, COUNT(c.id_chamado) AS total_chamados #resposta 3
FROM `datario.adm_central_atendimento_1746.chamado` AS c
JOIN `datario.dados_mestres.bairro` AS b
ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = "2023-04-01"
GROUP BY b.nome, b.subprefeitura
ORDER BY total_chamados DESC
LIMIT 3;

SELECT b.subprefeitura, COUNT(c.id_chamado) AS total_chamados #Resposta 4
FROM `datario.adm_central_atendimento_1746.chamado` AS c
JOIN `datario.dados_mestres.bairro` AS b
ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = "2023-04-01"
GROUP BY b.subprefeitura
ORDER BY total_chamados DESC
LIMIT 1;


SELECT * #Resposta 5
FROM `datario.adm_central_atendimento_1746.chamado` AS c 
LEFT JOIN `datario.dados_mestres.bairro` AS b
ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = "2023-04-01"
AND b.id_bairro IS NULL;


SELECT COUNT(*) AS total_chamados #questão 6
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE subtipo = 'Perturbação do sossego'
AND data_inicio BETWEEN '2022-01-01' AND '2023-12-31';


SELECT #Resposta 7
    chamado.id_chamado, 
    chamado.data_inicio, 
    MIN(evento.evento) AS evento,  
    MIN(evento.data_inicial) AS data_inicial,  
    MIN(evento.data_final) AS data_final  
FROM `datario.adm_central_atendimento_1746.chamado` AS chamado
JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS evento
ON chamado.data_inicio BETWEEN evento.data_inicial AND evento.data_final
WHERE chamado.subtipo = 'Perturbação do sossego'
GROUP BY chamado.id_chamado, chamado.data_inicio;

#resposta 8
SELECT evento, COUNT(id_chamado) AS num_chamados #Resposta 8
FROM (
    SELECT 
        chamado.id_chamado, 
        MIN(evento.evento) AS evento  
    FROM `datario.adm_central_atendimento_1746.chamado` AS chamado
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS evento
    ON chamado.data_inicio BETWEEN evento.data_inicial AND evento.data_final
    WHERE chamado.subtipo = 'Perturbação do sossego'
    GROUP BY chamado.id_chamado  
) AS subquery
GROUP BY evento;  

#9
WITH chamados AS ( #Resposta 9 
  SELECT
    evento.evento,
    COUNT(DISTINCT chamado.id_chamado) AS num_chamados
  FROM
    `datario.adm_central_atendimento_1746.chamado` AS chamado
  JOIN
    `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS evento
  ON
    chamado.data_inicio BETWEEN evento.data_inicial AND evento.data_final
  WHERE
    chamado.subtipo = 'Perturbação do sossego'
  GROUP BY
    evento 
), 

dias AS (
  SELECT
    evento.evento,
    SUM(DISTINCT DATE_DIFF(data_final, data_inicial, DAY) + 1) AS total_dias
  FROM
    `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS evento
  GROUP BY
    evento 
),

medias AS (
  SELECT
    chamados.evento,
    chamados.num_chamados,
    dias.total_dias,
    chamados.num_chamados / dias.total_dias AS media_diaria
  FROM
    chamados
  JOIN
    dias
  ON
    chamados.evento = dias.evento
)

SELECT *
FROM
  medias
WHERE
  media_diaria = (SELECT MAX(media_diaria) FROM medias);


#10
WITH chamados AS ( #Resposta 10
  SELECT
    evento.evento,
    COUNT(DISTINCT chamado.id_chamado) AS num_chamados
  FROM
    `datario.adm_central_atendimento_1746.chamado` AS chamado
  JOIN
    `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS evento
  ON
    chamado.data_inicio BETWEEN evento.data_inicial AND evento.data_final
  WHERE
    chamado.subtipo = 'Perturbação do sossego'
  GROUP BY
    evento 
), 

dias AS (
  SELECT
    evento.evento,
    SUM(DISTINCT DATE_DIFF(data_final, data_inicial, DAY) + 1) AS total_dias
  FROM
    `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS evento
  GROUP BY
    evento 
),

subtipo_periodo AS (
  SELECT
    COUNT(DISTINCT id_chamado) AS total_chamados,
    DATE_DIFF('2023-12-31', '2022-01-01', DAY) + 1 AS total_dias
  FROM 
    `datario.adm_central_atendimento_1746.chamado`
  WHERE 
    subtipo = 'Perturbação do sossego'
    AND data_inicio BETWEEN '2022-01-01' AND '2023-12-31'
)

SELECT
  chamados.evento,
  chamados.num_chamados,
  dias.total_dias,
  chamados.num_chamados / dias.total_dias AS media_diaria
FROM 
  chamados
JOIN 
  dias ON chamados.evento = dias.evento

UNION ALL

SELECT
  'Total de Chamados' AS evento,
  total_chamados,
  total_dias,
  total_chamados / total_dias AS media_diaria
FROM 
  subtipo_periodo;

