fetch('http://localhost:5000/alunos')
    .then(response => response.json())
    .then(data => {
        const produtos = document.getElementById('produtos');
        data.forEach(produtos => {
            const item = document.createElement('li');
            item.textContent = `ID: ${produtos.id} | Nome: ${produtos.nome} | Idade: ${produtos.preco}`;
            lista.appendChild(item);
        });
    })
.catch(error => {
console.error('Erro ao buscar alunos:', error);
});