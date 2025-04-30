In database creation add index to the following(queries are below):
-- Employees
CREATE INDEX idx_employees_name ON Employees(name);

-- Projects
CREATE INDEX idx_project_name ON Project(project_name);

-- Sites
CREATE INDEX idx_site_location ON Site(location);

-- Task
CREATE INDEX idx_task_projectid ON Task(project_id);
CREATE INDEX idx_task_status ON Task(status);
CREATE INDEX idx_task_assigneddate ON Task(assigned_date);

-- EmployeeTask (Many-to-Many between Employee and Task)
CREATE INDEX idx_employeetask_eid ON EmployeeTask(e_id);
CREATE INDEX idx_employeetask_taskid ON EmployeeTask(task_id);

-- ProjectSite (Many-to-Many between Project and Site)
CREATE INDEX idx_projectsite_projectid ON ProjectSite(project_id);
CREATE INDEX idx_projectsite_siteid ON ProjectSite(site_id);

-- EmployeeProject (Many-to-Many between Employee and Project)
CREATE INDEX idx_emp_proj_eid ON EmployeeProject(e_id);
CREATE INDEX idx_emp_proj_projectid ON EmployeeProject(project_id);
