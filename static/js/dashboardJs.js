const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
});



// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll('.sub-title').forEach(item => {
//         item.addEventListener('click', (e) => {
//             e.preventDefault();

//             const parent = e.currentTarget;
//             const submenu = parent.nextElementSibling; // Find the next sibling element

//             // Check if the submenu is currently active
//             const isActive = submenu.classList.contains('active');

//             document.querySelectorAll('.sub-menu').forEach(menu => {
//                 menu.classList.remove('active');
//             });

//             // Toggle the corresponding .sub-title and .sub-menu
//             if (!isActive) {
//                 submenu.classList.add('active');

//                 // parent.classList.add('active');
//             }
//         });
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    // Handle sub-menu toggling
    document.querySelectorAll('.sub-title').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            const parent = e.currentTarget;
            const submenu = parent.nextElementSibling; // Find the next sibling element

            // Check if the submenu is currently active
            const isActive = submenu.classList.contains('active');

            document.querySelectorAll('.sub-menu').forEach(menu => {
                menu.classList.remove('active');
            });

            // Toggle the corresponding .sub-title and .sub-menu
            if (!isActive) {
                submenu.classList.add('active');
            }
        });
    });

    // Ensure sub-items can handle active state and allow navigation
    const subItems = document.querySelectorAll('.sub-item > a');
    subItems.forEach(subItem => {
        subItem.addEventListener('click', (e) => {
            subItems.forEach(item => item.parentElement.classList.remove('active'));
            subItem.parentElement.classList.add('active');
            // Allow navigation to continue
        });
    });
});

// document.addEventListener('DOMContentLoaded', () => {
//     const subTitles = document.querySelectorAll('.sub-title > a');
//     const subItems = document.querySelectorAll('.sub-item > a');

//     subTitles.forEach(subTitle => {
//         subTitle.addEventListener('click', (e) => {
//             e.preventDefault();
//             const parent = subTitle.parentElement;
//             const submenu = parent.querySelector('.sub-menu');

//             // Remove 'active' class from all other sub-menus and sub-titles
//             document.querySelectorAll('.sub-title').forEach(title => {
//                 if (title !== parent) {
//                     title.classList.remove('active');
//                     title.querySelector('.sub-menu').classList.remove('active');
//                 }
//             });

//             // Toggle the active state of the clicked sub-menu
//             submenu.classList.toggle('active');
//         });
//     });

//     subItems.forEach(subItem => {
//         subItem.addEventListener('click', (e) => {
//             subItems.forEach(item => item.parentElement.classList.remove('active'));
//             subItem.parentElement.classList.add('active');
//         });
//     });
// });

// ==================================Sub-items active different approach======================================

// // Select all .sub-title elements
// const subTitles = document.querySelectorAll('.sub-title');

// // Iterate over each .sub-title element
// subTitles.forEach(subTitle => {
//     // Add a click event listener to each .sub-title element
//     subTitle.addEventListener('click', (e) => {
//         const parent = e.currentTarget;
//         const submenu = parent.nextElementSibling; // Find the next sibling element (.sub-menu)

//         // Remove 'active' class from all other .sub-menu elements
//         document.querySelectorAll('.sub-menu').forEach(menu => {
//             if (menu !== submenu) {
//                 menu.classList.remove('active');
//             }
//         });

//         // Toggle the active state of the clicked .sub-menu
//         submenu.classList.toggle('active');
//     });
// });

// // Handle sub-item click events to maintain active state and allow hyperlink redirection
// const subItems = document.querySelectorAll('.sub-item');

// subItems.forEach(subItem => {
//     subItem.addEventListener('click', (e) => {
//         // Remove 'active' class from all other sub-items
//         subItems.forEach(item => item.classList.remove('active'));

//         // Add 'active' class to the clicked sub-item
//         subItem.classList.add('active');
//     });
// });




// ==================================Sub-items active======================================
// subItems.forEach(item => {
//     item.addEventListener('click', (e) => {
//         subItems.forEach(subItem => {
//             subItem.classList.remove('active');
//         });
//         item.classList.add('active');
//         e.stopPropagation(); // Prevents the submenu from closing
//     });
// });
// ==================================Profile Pic Dropdown======================================
// function toggleDropdown() {
//     var dropdown = document.getElementById("myDropdown");
//     dropdown.classList.toggle("show");
//   }

//   // Close the dropdown if the user clicks outside of it
//   window.onclick = function(event) {
//     if (!event.target.matches('.dropbtn')) {
//       var dropdowns = document.getElementsByClassName("dropdown-content");
//       for (var i = 0; i < dropdowns.length; i++) {
//         var openDropdown = dropdowns[i];
//         if (openDropdown.classList.contains('show')) {
//           openDropdown.classList.remove('show');
//         }
//       }
//     }
//   }