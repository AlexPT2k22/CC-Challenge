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

  async function get_data(){
    const url = status_filter ? `${apiBaseUrl}/projects?status=${status_filter}` : apiBaseUrl+"/projects"
    const request = await fetch(url)
    const data = await request.json()
    projects = data
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
      <h2>Projektliste implementieren</h2>
      <p>
        Lade die Projekte direkt von der FastAPI, sortiere sie nach Datum und
        ergaenze einen Statusfilter. </p>
        <select bind:value={status_filter} on:change={get_data}>
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

