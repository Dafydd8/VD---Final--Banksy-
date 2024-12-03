<script>

  import * as d3 from "d3"
  import { onMount } from "svelte"
  import { parse } from "papaparse";
  import obras_raw from "/src/data/Datos_Banksy.csv?raw"
  import main_obras_raw from "/src/data/main_obras.csv?raw"; // Importa el archivo como texto

  const options = {
    delimiter: ";", // Configura el delimitador como punto y coma
    header: true,   // Opcional: Indica si el CSV tiene encabezados
  };

  const processCSV = (raw) => {
    const parsedData = parse(main_obras_raw, options);
    return parsedData.data;
  };

  const main_obras = processCSV(main_obras_raw);
  const main_obras1 = main_obras.slice(0, 5);
  const main_obras2 = main_obras.slice(5, 10);

  const obras = processCSV(obras_raw);
  
  const valores = [];
  for (let i = 0; i < main_obras.length; i++) {
    valores.push(parseInt(main_obras[i].Valor));
  }

  const tematicas = {
    "Violencia": "ramo.png",
    "Justicia social": "globo.png",
    "Política": "monito.png",
    "Capitalismo": "rata.png",
    "Medio ambiente": "flor.png",
  }

  const tecnicas = {
    "Stencil": "orange",
    "Óleo sobre lienzo": "red",
    "Mural": "yellow",
    "Instalación": "green"
  }

  const textos_detective = [
    "Empecemos nuestra búsqueda, que será extensa pero valdrá la pena! Este mapa lo fui armando a través de los años, donde podés ver todas las obras de Banksy de las que tenemos registro hasta hoy en día. ¡Son más de 115!",
    "Las primeras obras de Banksy se encuentran en la que suponemos es su ciudad natal, Bristol.",
    "Mmm... no encontramos nada muy revelador... sigamos nuestro viaje. Veamos otro de los lugares que mas frecuenta Banksy a la hora de pintar.",
    "A nuestro artista misterioso le gusta Nueva York. Es la ciudad por excelencia para criticar al capitalismo salvaje.",
    "Nada aún... es realmente sigiloso. No perdamos más tiempo y pasemos a nuestra siguiente pista.",
    "Estamos en Jerusalén. Banksy aboga fuertemente por la paz y Medio Oriente es foco de muchas de sus obras que hacen alusión a esta causa.",
    "No vimos nada, pero siento que estamos cerca. ¡Nos avisan que lo han visto en Australia! ¡Rápido, que no se escape!",
    "Llegamos a Melbourne. A ver qué descubrimos...",
    "Increíble, es realmente bueno escondiéndose. Tranquilo, aún nos queda un lugar más donde buscar.",
    "Estamos en Disneyland, California. ¡Qué lugar para una obra de este estilo! Vaya que hace llegar su mensaje",
    "No puedo creerlo, realmente no pudimos descubrirlo. Creo que la identidad de Banksy permanecerá en secreto por mucho tiempo más. Mientras tanto, podés seguir aprendiendo sobre su arte."
  ]

  let diapositiva_actual = 1;
  //console.log("VALORES ", d3.min(valores), d3.max(valores));
  let cant_splash = d3
    .scaleLinear()
    .domain([d3.min(valores), d3.max(valores)])
    .range([1, 4])

  function loadFlourishScrolly() {
    const script = document.createElement('script')
    script.src = "https://cdn.flourish.rocks/flourish-scrolly-v3.1.0.min.js"
    script.type = "text/javascript"
    script.onload = () => initFlourishScrolly()
    document.body.appendChild(script)
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }else{
          entry.target.classList.remove("visible");
        }
      });
    },
    {
      threshold: 0.10, // La sección debe estar al menos un 10% visible para activarse
    }
  );

  onMount(() => {
    console.log("Página cargada");
    loadFlourishScrolly()

    const totalPages = 6; // Número total de páginas
    let currentPage = Math.min(Math.floor(document.documentElement.scrollTop / window.innerHeight), totalPages - 1);

    console.log("pos", currentPage);
    let isScrolling = false; // Evita desplazamientos repetidos mientras la animación está en curso

    const handleWheel = (event) => {
      let posScroll = window.scrollY + window.innerHeight;
      if (isScrolling || posScroll > totalPages*window.innerHeight) return; // No hacer nada si ya estamos desplazando o estamos fuera de las primeras paginas

      const newPage =
        event.deltaY > 0
          ? Math.min(currentPage + 1, totalPages - 1) // Avanza si hay más páginas
          : Math.max(currentPage - 1, 0); // Retrocede si no estamos en la primera

      if (newPage !== currentPage) {
        currentPage = newPage;
        scrollToPage(currentPage);
      }
    };

    const scrollToPage = (page) => {
      isScrolling = true; // Bloquear más scrolls
      window.scrollTo({
        top: page * window.innerHeight,
        behavior: "instant",
      });
      // Liberar bloqueo después de la animación (duración típica de `smooth`)
      setTimeout(() => {
        isScrolling = false;
      }, 500);
    };

    window.addEventListener("wheel", handleWheel);

    // Selecciona todas las secciones con la clase 'fade-in'
    const pages = document.querySelectorAll(".page");
    pages.forEach((el) => observer.observe(el));

    const cards_obras = document.querySelectorAll(".obra");
    const dialogue = (document.querySelectorAll(".detective_dialogue"))[0];
    const observer_dialogue = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            diapositiva_actual = entry.target.id-1;
            dialogue.classList.add("visible");
          }else{
            dialogue.classList.remove("visible");
          }
        });
      },
      {
        threshold: 0.90, // La sección debe estar al menos un 50% visible para activarse
      }
    );

    cards_obras.forEach((el) => observer_dialogue.observe(el));


    return () => {
      elements.forEach((el) => observer.unobserve(el));
      window.removeEventListener("wheel", handleWheel);
    };

  });

</script>

<main>
  <section id="header" class="page">
    <h1 id="main_title" style="font-size:100px">Finding Banksy</h1>
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>

  </section>

  <section class="page">
    <img src="/images/inv_pointing.png" alt="detctive" style="max-height:50vh"/>
    <div class="text-container">
      <p>¡Ey! Vos debés ser el compañero que me asignaron en mi búsqueda de Banksy ¡Al fin llegas! Vamos, hay mucho en lo que tenés que ponerte al día.</p>
    </div>  
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>
  </section>

  <section class="page">
    <img src="/images/inv_actually.png" alt="detctive" style="max-height:50vh"/>
    <div class="text-container">
      <p>Banksy es un enigmático artista callejero británico, conocido por su arte provocador, crítico social y políticamente cargado, que combina ironía, sátira y mensajes contundentes. Aunque su verdadera identidad sigue siendo un misterio, Banksy ha ganado reconocimiento global como uno de los artistas más influyentes del mundo contemporáneo.</p>
    </div>  
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>
  </section>

  <section class="page">
    <img src="/images/inv_lupa.png" alt="detctive" style="max-height:50vh"/>
    <div class="text-container">
      <p>Nuestra misión es tratar de descrubrir quién es y desenmascararlo. Para eso, vamos a seguir su rastro a través del mundo, pasando por sus obras más emblemáticas. Veamos que podemos descubrir sobre él.</p>
    </div>  
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>
  </section>

  <section class="page" style="flex-direction:column">
    <div id="primer_dialogo" style="width:fit-content;">
      <img src="/images/detective_round.png" alt="detective" style="width:80px"/>
      <p>Te voy a mostrar la codificación secreta que desarrollé para la información que voy recopilando sobre las obras.</p>
    </div>
    <img src="/images/cheat_sheet.png" alt="cheat sheet" style="max-height:65vh"/>
    <!---<img src="/images/down_arrows.png" alt="flechas" class="flechas"/>--->
  </section>

  <section class="page" style="flex-direction:column; gap:0px !important">
    <div id="primer_dialogo" style="width:fit-content">
      <img src="/images/detective_round.png" alt="detective" style="width:80px"/>
      <p>Estas son las obras que vamos a visitar en nuestra búsqueda. Intenta memorizarlas lo más que puedas para poder seguir el ritmo de la investigación. ¡Emprendamos nuestra aventura! </p>
    </div>
    <div class="grid_obras">
      {#each main_obras1 as obra, index}
        <div class="obra_beggining" style="width:20%">
          <div class="codificacion" style="width:60% !important">
            <img src="/images/{tematicas[obra.Motivo]}" alt="{obra.Motivo}" class="tematica {obra.Estado == 'Vandalizada' ? 'vandalizada' : ''}" />
            <img src="/images/{Math.round(cant_splash(parseInt(obra.Valor)))}_{tecnicas[obra.Tecnica]}.png" alt="{obra.Tecnica}" class="tecnica" />
            {#if obra.Estado == "Removida"}
              <img src="/images/cruz.png" alt="Removida" style="position:absolute; z-index:2; width:30%"/>
            {/if}
          </div>
          <h3 style="position:relative; text-align:center">{obra.Titulo}</h3>
        </div>
      {/each}
    </div>
    <div class="grid_obras">
      {#each main_obras2 as obra, index}
        <div class="obra_beggining" style="width:20%">
          <div class="codificacion" style="width:60% !important">
            <img src="/images/{tematicas[obra.Motivo]}" alt="{obra.Motivo}" class="tematica {obra.Estado == 'Vandalizada' ? 'vandalizada' : ''}" />
            <img src="/images/{Math.round(cant_splash(parseInt(obra.Valor)))}_{tecnicas[obra.Tecnica]}.png" alt="{obra.Tecnica}" class="tecnica" />
            {#if obra.Estado == "Removida"}
              <img src="/images/cruz.png" alt="Removida" style="position:absolute; z-index:2; width:30%"/>
            {/if}
          </div>
          <h3 style="position:relative; text-align:center">{obra.Titulo}</h3>
        </div>
      {/each}
    </div>
    <!---<img src="/images/down_arrows.png" alt="flechas" class="flechas"/>-->
  </section>

<!--
  <section class="page">
    <img src="/images/detective_ground.png" alt="detctive" style="max-height:50vh"/>
    <div class="text-container">
      <p>¡Vamos, no perdamos más tiempo!</p>
    </div>  
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>
  </section>
  -->

  <div id="my-wrapper">
<!-- 
  <div class="detective_dialogue">
    <img src="/images/detective_round.png" alt="detective" style="width:12.5%"/>
    <p>{textos_detective[diapositiva_actual]}</p>
  </div>
    -->

    <div class="flourish-embed" data-src="story/2739950" data-url="https://flo.uri.sh/story/2739950/embed" data-height="100vh">

    </div>
    {#each main_obras as obra, index}
      <a class="card detective_speech" href={"#story/2739950/slide-" + (index*3 + 1)}>
        <img src="/images/detective_round.png" alt="detective" style="width:30%"/>
        <p>{textos_detective[index*2]}</p>
      </a>

      <a class="card obra" href={"#story/2739950/slide-" + (index*3 + 2)} id="{index*2+2}">
        <div class="obra_info">
          <div class="codificacion">
            <img src="/images/{tematicas[obra.Motivo]}" alt="{obra.Motivo}" class="tematica {obra.Estado == 'Vandalizada' ? 'vandalizada' : ''}" />
            <img src="/images/{Math.round(cant_splash(parseInt(obra.Valor)))}_{tecnicas[obra.Tecnica]}.png" alt="{obra.Tecnica}" class="tecnica" />
            {#if obra.Estado == "Removida"}
              <img src="/images/cruz.png" alt="Removida" style="position:absolute; z-index:2; width:30%"/>
            {/if}
          </div>
          <div style="width:75%">
            <h3 style="position:relative; font-size:30px; text-align:center">{obra.Titulo}</h3>
          </div>
        </div>
        <img src="{obra.Imagen}" alt="imagen obra" class="obra_imagen" style="width:100%; border-radius:20px"/>
      </a>

      <a class="card detective_speech" href={"#story/2739950/slide-" + (index*3 + 3)}>
        <img src="/images/detective_round.png" alt="detective" style="width:30%"/>
        <p>{textos_detective[index*2+1]} {obra.Texto}</p>
      </a>

    {/each}
    <a class="card detective_speech" href="#story/2739950/slide-{(textos_detective.length-1)*3/2+1}">
      <img src="/images/detective_round.png" alt="detective" style="width:30%"/>
      <p>{textos_detective[textos_detective.length-1]}</p>
    </a>
  </div>

  <section class="page">
    <h1>THE END</h1>
  </section>

</main>

<style>
  .page {
    position: relative;
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    scroll-snap-align: start; /* Para suavizar la navegación si el usuario hace scroll manual */
    opacity: 0;
    transition: opacity 1s ease;
  }

  .detective_dialogue {
    width: 610px;
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    display: flex;
    flex-direction: row;
    left:30px;
    top:20px;
    align-items: center;
    justify-content: flex-start;
    z-index:3;
    padding: 10px;
    gap: 15px;
    border-radius: 20px;
    opacity: 0; 
    transition: opacity 1s ease;
  }
  
  #primer_dialogo {
    max-width: 90vw;
    position:relative;
    background-color: rgba(58, 58, 75, 1);
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 10px;
    gap: 15px;
    border-radius: 20px;
    z-index: 100;
  }

  .grid_obras {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    flex-direction: row;
    max-width: 90vw;
    height: fit-content;
  }

  .obra_beggining {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  #my-wrapper {
    background: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 100vw;
    padding:0% !important;
    margin-bottom: 0px !important;
    background-color: rgba(0,0,0,0) !important;
  }

  .flourish-embed {
    margin: auto;
    width: 50vw;
    transform: translateX(-50%);
  }

  .card {
    transform: translateX(62.5%);
    height: 50%;
    width: 40vw;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(58, 58, 75, 1);
    margin-top: 50%;
    margin-bottom: 50%; 
    margin-left: auto;
    margin-right: auto;
    border-radius: 20px;
  }

  .detective_speech {
    flex-direction: row;
    gap: 30px;
    justify-content: flex-start;
    align-items: self-start;
  }

  .obra {
    flex-direction: column;
  }

  .card p {
    position: relative;
    max-width: 70%;
    text-align: justify;
  }

  .codificacion {
    width:25% !important;
    aspect-ratio: 1/1;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .obra_info {
    width:100%;
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .tematica {
    position: absolute;
    z-index: 1;
    width: 60%;
  }

  .vandalizada {
    mask-image: repeating-linear-gradient(135deg, black 0%, black 2.5%, transparent 2.5%, transparent 5%);
    -webkit-mask-size: 20px 20px; /* Ajusta el tamaño de las líneas */
    mask-size: 100% 100%;
  }

  .tecnica {
    position: relative;
    width: 100%;
  }

  .text-container {
    position: relative;
    background-color: rgba(58, 58, 75, 1);
    max-width: 50%;
    padding: 20px;
    border-radius: 20px;
  }

  .flechas {
    position: absolute;
    bottom: 7%;
    width: 5%;
    animation: flash 1s ease infinite alternate;
  }

  @keyframes flash {
    from { opacity: 1; }	
    to { opacity: 0.1; }
  }

  h1 {
    color: #ffffff;
    font-weight: 700;
    font-family: "Lacquer", system-ui;
  }
  
  h3{
    margin: 0px;
    padding: 0px;
    text-align: center;
    min-height: 3em;
    line-height: 1.5;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-family: 'Lacquer', sans-serif;
    font-size: 20px;
  }

  p {
    color: #ffffff;
    font-family: 'Nunito', sans-serif;
  }

</style>