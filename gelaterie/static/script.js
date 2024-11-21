// Toggle the display of product categories or sponsors
function toggleDetails(category) {
    // Get all the details panels
    const panels = document.querySelectorAll('.details-panel');
    
    // Check if the clicked panel is already open
    const panel = document.getElementById(category);
    
    // If the panel is visible, hide it, otherwise show it
    if (panel.style.display === 'block') {
        panel.style.display = 'none';
    } else {
        // Hide all panels first
        panels.forEach(function(p) {
            p.style.display = 'none';
        });
        
        // Show the selected panel
        panel.style.display = 'block';
    }
}

// Toggle the visibility of the sponsors in the footer
function toggleSponsors() {
    const sponsorPanel = document.getElementById('footer-sponsors');
    if (sponsorPanel) {
        sponsorPanel.style.display = sponsorPanel.style.display === 'none' ? 'block' : 'none';
    }
}
