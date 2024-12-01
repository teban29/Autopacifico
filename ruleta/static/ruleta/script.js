let container = document.querySelector(".container");
let btn = document.getElementById("spin");

// Configurar probabilidades (en el mismo orden que las casillas)
let premios = [
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $50,000", probabilidad: 8 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $100,000", probabilidad: 6 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $150,000", probabilidad: 4 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $200,000", probabilidad: 2 },
];

function seleccionarPremio() {
    let total = premios.reduce((sum, premio) => sum + premio.probabilidad, 0);
    let random = Math.random() * total;

    let acumulado = 0;
    for (let i = 0; i < premios.length; i++) {
        acumulado += premios[i].probabilidad;
        if (random <= acumulado) {
            return i; // Retorna el índice del premio seleccionado
        }
    }
}

btn.onclick = function () {
    let seleccionado = seleccionarPremio(); // Determina el índice del premio
    let gradosPorSegmento = 360 / premios.length; // Grados de cada segmento
    let gradosSeleccionados = gradosPorSegmento * seleccionado; // Grados donde comienza el segmento seleccionado
    let ajusteInicial = 22.5; // Compensación para alinear el primer segmento con la flecha
    let rotacionFinal = (360 * 5) + (360 - (gradosSeleccionados + ajusteInicial)); // Giros completos + ajuste

    // Rotar la ruleta
    container.style.transform = `rotate(${rotacionFinal}deg)`;

    setTimeout(() => {
        // Mostrar el premio seleccionado después de la animación
        console.log(`Premio seleccionado: ${premios[seleccionado].nombre}`);

        // Guardar resultado en Django
        fetch(resultadoUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ premio: premios[seleccionado].nombre }),
        })
            .then(response => {
                if (response.ok) {
                    console.log("Resultado enviado correctamente al servidor.");
                    return response.json(); // Obtener la respuesta del servidor
                } else {
                    console.error("Error al enviar el resultado al servidor.");
                }
            })
            .then(data => {
                console.log("Respuesta del servidor:", data);
            })
            .catch(error => console.error("Error en la solicitud:", error));
    }, 5000); // Espera el tiempo de la animación antes de enviar el resultado
};
