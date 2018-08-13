use encode;
SELECT experiment.id, experiment_type.name, biosample.name, biosample_term_name.name, experiment.cell_cicle, experiment.treatments, experiment.genetic_modifications,  internal_status.name, project.name, experiment_has_assembly.assembly_id, organism.name, experiment.red_errors, experiment.orange_errors, experiment.yellow_errors, experiment.replicates, experiment.replication_type
FROM experiment 
LEFT JOIN experiment_type ON experiment.experiment_type_id = experiment_type.id
LEFT JOIN internal_status ON experiment.internal_status_id = internal_status.id
LEFT JOIN status ON experiment.status_id = status.id
LEFT JOIN biosample_term_name ON experiment.biosample_term_name_id = biosample_term_name.id
LEFT JOIN biosample ON biosample_term_name.biosample_id = biosample.id
LEFT JOIN experiment_has_assembly ON experiment.id = experiment_has_assembly.experiment_id
LEFT JOIN organism ON experiment.organism_id = organism.id
LEFT JOIN project ON experiment.project_id = project.id
WHERE (experiment_has_assembly.assembly_id = 'GRCh38'
AND organism.name = 'Homo sapiens'
AND experiment.cell_cicle = '-'
AND experiment.treatments = '-'
AND experiment.red_errors = '0'
AND internal_status.name = 'pipeline completed'
AND experiment.replicates >= 2
AND experiment.replication_type != 'unreplicated'
)
OR 
(experiment_has_assembly.assembly_id = 'GRCh38'
AND organism.name = 'Homo sapiens'
AND experiment.cell_cicle = '-'
AND experiment.treatments = '-'
AND experiment.red_errors = '0'
AND internal_status.name = 'release ready'
AND experiment.replicates >= 2
AND experiment.replication_type != 'unreplicated'
)
ORDER BY biosample.name, biosample_term_name.name, experiment_type.name, experiment.cell_cicle, experiment.treatments, experiment.genetic_modifications, experiment.red_errors, experiment.orange_errors,  experiment.yellow_errors;

