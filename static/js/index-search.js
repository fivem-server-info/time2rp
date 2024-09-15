console.log(document.getElementById('search')); // Should log the input element


// document.getElementById('search').addEventListener('input', function() {
//     const searchTerm = this.value.toLowerCase();
//     console.log("Search Term: ", searchTerm); // Debugging line
//     const rows = document.querySelectorAll('#player-table tr:not(#table-header)');
    
//     rows.forEach(row => {
//         const idCell = row.querySelector('.table-id').textContent.toLowerCase();
//         const nameCell = row.querySelector('.table-log').textContent.toLowerCase();
//         console.log("ID Cell: ", idCell, " Name Cell: ", nameCell); // Debugging line
        
//         // Display row if search term matches either ID or name
//         if (idCell.includes(searchTerm) || nameCell.includes(searchTerm)) {
//             row.style.display = ''; // Show row
//         } else {
//             row.style.display = 'none'; // Hide row
//         }
//     });
// });
