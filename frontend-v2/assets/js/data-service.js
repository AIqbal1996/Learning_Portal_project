/*
  Data access layer for Learning Portal V2.
  It first tries the optional Python JSON adapter. If not running, it falls back
  to curated demo data so executives can still see the V2 experience.
*/
window.LearningDataService = (() => {
  const API_BASE = window.LEARNING_API_BASE || "";

  const categoryMapping = {
    "Data Engineering": ["Data Engineering", "Data Architecture", "Data Warehouse", "ETL", "DataOps", "MLOps", "Data Management", "Data Mangement", "Datastage", "Airflow", "Data Science", "GCP Data Engineer", "PubSub", "Dataproc"],
    "Azure": ["Azure", "Cosmos DB", "Logic App", "MS Fabric", "SSAS", "SSIS", "PubSub"],
    "AWS": ["AWS"],
    "Spark": ["Spark", "PySpark", "Scala", "Hadoop", "Dataproc"],
    "Snowflake": ["Snowflake"],
    "Power BI": ["Power BI", "Power Platform", "Power Automate", "Power Apps", "Tableau"],
    "SQL": ["SQL", "MySQL", "Postgre", "MongoDB", "Teradata", "Kustos", "BigQuery"]
  };

  const demoCourses = [
    { id: "C-001", name: "Data Engineering Foundations", category: "Data Engineering", durationHours: 8, level: "Beginner", link: "https://example.com/data-engineering", description: "Build a credible foundation in pipelines, warehouses, ETL, and data quality controls." },
    { id: "C-002", name: "Azure Data Factory for Enterprise Teams", category: "Azure", durationHours: 12, level: "Intermediate", link: "https://example.com/azure", description: "Design modern cloud data flows using Azure-native services and governance patterns." },
    { id: "C-003", name: "AWS Data Engineering Immersion", category: "AWS", durationHours: 10, level: "Intermediate", link: "https://example.com/aws", description: "Learn data lake, Glue, Redshift, and operational patterns for scalable analytics." },
    { id: "C-004", name: "Spark and PySpark Performance", category: "Spark", durationHours: 9, level: "Advanced", link: "https://example.com/spark", description: "Optimize large-scale jobs with partitioning, joins, caching, and practical debugging." },
    { id: "C-005", name: "Snowflake Zero to Production", category: "Snowflake", durationHours: 7, level: "Intermediate", link: "https://example.com/snowflake", description: "Move from schema design to secure sharing, cost controls, and warehouse tuning." },
    { id: "C-006", name: "Power BI Executive Dashboards", category: "Power BI", durationHours: 6, level: "Beginner", link: "https://example.com/powerbi", description: "Create high-trust KPI dashboards for business, finance, and operations stakeholders." },
    { id: "C-007", name: "SQL for Analytics Engineering", category: "SQL", durationHours: 11, level: "Beginner", link: "https://example.com/sql", description: "Use SQL for data modeling, diagnostics, cohort analysis, and high-confidence reporting." },
    { id: "C-008", name: "MLOps and DataOps Delivery Model", category: "Data Engineering", durationHours: 14, level: "Advanced", link: "https://example.com/mlops", description: "Align experimentation, production deployment, monitoring, and governance workflows." }
  ];

  const demoWorkbooks = {
    training: {
      title: "Training List",
      subtitle: "Curated learning sheets with downloadable records.",
      sheets: [
        { name: "Core Programs", rows: [
          { Track: "Data Engineering", Owner: "L&D Team", Audience: "Students + Corporate", Status: "Active", Duration: "6 weeks" },
          { Track: "Cloud Data", Owner: "Platform Team", Audience: "Corporate", Status: "Active", Duration: "4 weeks" },
          { Track: "Analytics", Owner: "BI Team", Audience: "Students", Status: "Pilot", Duration: "3 weeks" }
        ]},
        { name: "Role Paths", rows: [
          { Role: "Data Analyst", Modules: "SQL, Power BI, Statistics", Level: "Foundation", Outcome: "Dashboard delivery" },
          { Role: "Data Engineer", Modules: "ETL, Spark, Cloud", Level: "Intermediate", Outcome: "Pipeline delivery" }
        ]}
      ]
    },
    pilots: {
      title: "Pilots",
      subtitle: "Track pilot programs, rollout readiness, and stakeholder actions.",
      sheets: [
        { name: "Pilot Tracker", rows: [
          { Pilot: "Campus Upskilling", Sponsor: "University Team", Stage: "Discovery", Health: "On Track" },
          { Pilot: "Enterprise Academy", Sponsor: "Corporate HR", Stage: "Implementation", Health: "On Track" },
          { Pilot: "Assessment Benchmark", Sponsor: "Engineering", Stage: "Validation", Health: "Needs Review" }
        ]}
      ]
    },
    assessments: {
      title: "HackerRank Assessment",
      subtitle: "Assessment sheets with quick search and export support.",
      sheets: [
        { name: "Coding", rows: [
          { Skill: "Python", Difficulty: "Medium", Attempts: 42, AvgScore: "78%" },
          { Skill: "SQL", Difficulty: "Easy", Attempts: 56, AvgScore: "84%" },
          { Skill: "Spark", Difficulty: "Hard", Attempts: 18, AvgScore: "68%" }
        ]},
        { name: "Analytics", rows: [
          { Skill: "Power BI", Difficulty: "Medium", Attempts: 21, AvgScore: "76%" },
          { Skill: "Data Modeling", Difficulty: "Medium", Attempts: 24, AvgScore: "72%" }
        ]}
      ]
    }
  };

  async function fetchJson(path, fallback) {
    try {
      const response = await fetch(`${API_BASE}${path}`, { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      return fallback;
    }
  }

  function normalizeCourse(raw, index) {
    const name = raw.name || raw["Course Name"] || raw.course_name || `Course ${index + 1}`;
    const durationHours = Number(raw.durationHours || raw["Duration(Hr)"] || raw.duration_hr || 0) || 0;
    const inferredCategory = inferCategory(name, raw.category);
    return {
      id: raw.id || `COURSE-${String(index + 1).padStart(3, "0")}`,
      name,
      category: inferredCategory,
      durationHours,
      level: raw.level || (durationHours >= 12 ? "Advanced" : durationHours >= 8 ? "Intermediate" : "Beginner"),
      link: raw.link || raw.Link || "",
      description: raw.description || describeCourse(name, inferredCategory)
    };
  }

  function inferCategory(name, fallback) {
    if (fallback) return fallback;
    const lowerName = String(name).toLowerCase();
    const match = Object.entries(categoryMapping).find(([, keywords]) =>
      keywords.some(keyword => lowerName.includes(keyword.toLowerCase()))
    );
    return match ? match[0] : "Data Engineering";
  }

  function describeCourse(name, category) {
    return `Focused ${category} learning experience designed for practical application, retention, and role readiness.`;
  }

  async function getCourses() {
    const payload = await fetchJson("/api/courses", { courses: demoCourses });
    const courses = Array.isArray(payload) ? payload : payload.courses || demoCourses;
    return courses.map(normalizeCourse);
  }

  async function getWorkbook(type) {
    return fetchJson(`/api/workbooks/${type}`, demoWorkbooks[type] || { title: type, sheets: [] });
  }

  async function getSummary() {
    const courses = await getCourses();
    const totalHours = courses.reduce((sum, course) => sum + course.durationHours, 0);
    const categories = new Set(courses.map(course => course.category));
    return {
      totalCourses: courses.length,
      totalHours,
      totalCategories: categories.size,
      completionFocus: 82
    };
  }

  return { getCourses, getWorkbook, getSummary, categoryMapping };
})();
