$(document).ready(function() {
    $('.delete-cupcake').click(deleteTodo)
});


async function deleteTodo() {
        const id = $(this).data('id')
        await axios.delete(`api/cupcakes/${id}`)
        $(this).parent().remove()
}