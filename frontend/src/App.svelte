<script lang="ts">
  import { onMount } from "svelte";
  import Header from "./lib/Header.svelte";

  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

  let status_filter = ""

  interface projects_interface {
    id: number;
    customer_id: number;
    date: string;
    task: string;
    location: string | null;
    description: string | null;
    status: string;
  }

  let projects: projects_interface[] = [];
  let new_project: projects_interface = {
    id: 0,
    customer_id: 0,
    date: "",
    task: "",
    location: null,
    description: null,
    status: "",
  }

  async function get_data(){
    const url = status_filter ? `${apiBaseUrl}/projects?status=${status_filter}` : apiBaseUrl+"/projects"
    const request = await fetch(url)
    const data = await request.json()
    projects = data
  }

  async function submitProject() {
    try {
      const request = await fetch(apiBaseUrl + "/projects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(new_project)
      })

      if (!request.ok) {
      const errorData = await request.json();
      throw new Error(errorData.detail || "Failed to create project");
      }

      new_project = {
      id: 0,
      customer_id: 0,
      date: "",
      task: "",
      location: null,
      description: null,
      status: ""
      };

      get_data()
      
    }catch(error){
      console.error("Error creating project:", error);
      alert("Failed to create project: " + error);
    }
  }

  onMount(get_data)
</script>

<Header />

<main class="page">
  <section class="toolbar">
    <div>
      <h1>Kanalprojekte</h1>
      <p>Projektuebersicht fuer Reinigung, Inspektion und Sanierung.</p>
    </div>
    <span class="api-pill">{apiBaseUrl}</span>
  </section>

  <section class="workbench" aria-label="Projektliste">
    <div class="empty-state">
    <h2>Add a Project</h2>
        <form on:submit|preventDefault={submitProject}>
        <label>
          Project ID
          <input type="number" bind:value={new_project.id} min="1" required>
        </label>
        <label>
          Customer_ID
          <input type="number" bind:value={new_project.customer_id} min="1" required>
        </label>
        <label>
          Date
          <input type="date" bind:value={new_project.date} required>
        </label>
        <label>
          Task
          <input type="text" bind:value={new_project.task} required>
        </label>
        <label>
          Location
          <input type="text" bind:value={new_project.location}>
        </label>
        <label>
          Description
          <input type="text" bind:value={new_project.description}>
        </label>
        <select bind:value={new_project.status} required>
          <option value="" disabled selected>Select status</option>
          <option value="open">Open</option>
          <option value="in progress">In progress</option>
          <option value="done">Done</option>
        </select>
        <button type="submit">Add Project</button>
        </form>

        <h2>List of all {projects.length} projects</h2>
        <select class="select_button" bind:value={status_filter} on:change={get_data}>
          <option value="">All statuses</option>
          <option value="open">Open</option>
          <option value="in progress">In progress</option>
          <option value="done">Done</option>
        </select>
        <table>
        <thead>
          <tr>
            <th>Project ID</th>
            <th>Customer_ID</th>
            <th>Date</th>
            <th>Task</th>
            <th>Location</th>
            <th>Description</th>
            <th>Status</th>
          </tr>
        </thead>
          <tbody>
            {#each projects as project (project.id)}
              <tr>
                <td>{project.id}</td>
                <td>{project.customer_id}</td>
                <td>{project.date}</td>
                <td>{project.task}</td>
                <td>{#if project.location != null}
                  {project.location}
                  {:else}
                  NULL
                {/if}</td>
                <td>{#if project.description != null}
                  {project.description}
                  {:else}
                  NULL
                {/if}</td>
                <td>{project.status}</td>
              </tr>
            {/each}
          </tbody>
        </table>
    </div>
  </section>
</main>

