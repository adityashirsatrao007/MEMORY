document.addEventListener('DOMContentLoaded', () => {
  initSearchModal();
  initVersionDropdown();
  initCollapsibleDirectories();
  initCodeCopyButtons();
  initSpotlightEffect();
  initMobileNav();
  initTableOfContentsActiveState();
});

/* ==========================================================================
   COMPONENT 4: INPUTS & GLOBAL SEARCH MODAL (Cmd+K / Slash)
   ========================================================================== */
function initSearchModal() {
  const searchTriggers = document.querySelectorAll('.js-search-trigger');
  const modalOverlay = document.getElementById('searchModalOverlay');
  const modalInput = document.getElementById('searchModalInput');
  const modalCloseBtn = document.getElementById('searchModalClose');
  const resultsContainer = document.getElementById('searchModalResults');
  
  const searchDatabase = [
    { title: "Introduction to Remix", url: "#introduction", excerpt: "Learn about the core values of Remix: server rendering, data loading, and mutations." },
    { title: "Data Loading (loader)", url: "#data-loading", excerpt: "Load data from the server inside your route component using loaders." },
    { title: "Data Mutations (action)", url: "#mutations", excerpt: "Perform server-side actions using HTML forms and actions." },
    { title: "Nested Routing", url: "#nested-routing", excerpt: "Render sub-layouts dynamically based on URL segments using Outlet." },
    { title: "Error Boundaries", url: "#error-boundaries", excerpt: "Catch errors globally or locally inside nested route error boundaries." }
  ];

  let selectedIndex = -1;
  let activeItems = [];

  // Open Modal
  function openModal() {
    modalOverlay.classList.add('active');
    modalOverlay.setAttribute('aria-hidden', 'false');
    setTimeout(() => modalInput.focus(), 50);
    document.body.style.overflow = 'hidden';
    renderResults("");
  }

  // Close Modal
  function closeModal() {
    modalOverlay.classList.remove('active');
    modalOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    modalInput.value = '';
    selectedIndex = -1;
    activeItems = [];
  }

  // Keyboard shortcut triggers: Cmd+K, Ctrl+K, or Slash "/"
  document.addEventListener('keydown', (e) => {
    const isEditing = ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName);
    if ((e.key === 'k' && (e.metaKey || e.ctrlKey)) || (e.key === '/' && !isEditing)) {
      e.preventDefault();
      openModal();
    }
  });

  searchTriggers.forEach(trigger => trigger.addEventListener('click', openModal));
  modalCloseBtn.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  // Modal Input Keyboard Handling & Result Filtering
  modalInput.addEventListener('input', (e) => {
    renderResults(e.target.value);
  });

  modalInput.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      navigateResults(1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      navigateResults(-1);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && activeItems[selectedIndex]) {
        selectResult(activeItems[selectedIndex]);
      } else if (activeItems.length > 0) {
        selectResult(activeItems[0]);
      }
    }
  });

  function renderResults(query) {
    resultsContainer.innerHTML = '';
    selectedIndex = -1;
    
    const filtered = searchDatabase.filter(item => {
      if (!query) return true;
      const q = query.toLowerCase();
      return item.title.toLowerCase().includes(q) || item.excerpt.toLowerCase().includes(q);
    });

    if (filtered.length === 0) {
      resultsContainer.innerHTML = '<div class="directory-empty">No results match your search query.</div>';
      activeItems = [];
      return;
    }

    activeItems = filtered;
    filtered.forEach((item, index) => {
      const div = document.createElement('div');
      div.className = 'search-result-item';
      div.setAttribute('role', 'option');
      div.setAttribute('id', `search-opt-${index}`);
      div.innerHTML = `
        <div class="search-result-title">${item.title}</div>
        <div class="search-result-excerpt">${item.excerpt}</div>
      `;
      div.addEventListener('click', () => selectResult(item));
      div.addEventListener('mouseover', () => {
        setSelection(index);
      });
      resultsContainer.appendChild(div);
    });
  }

  function setSelection(index) {
    const items = resultsContainer.querySelectorAll('.search-result-item');
    items.forEach(item => item.classList.remove('selected'));
    
    selectedIndex = index;
    if (index >= 0 && items[index]) {
      items[index].classList.add('selected');
      items[index].scrollIntoView({ block: 'nearest' });
      modalInput.setAttribute('aria-activedescendant', `search-opt-${index}`);
    } else {
      modalInput.removeAttribute('aria-activedescendant');
    }
  }

  function navigateResults(direction) {
    if (activeItems.length === 0) return;
    let nextIndex = selectedIndex + direction;
    if (nextIndex < 0) nextIndex = activeItems.length - 1;
    if (nextIndex >= activeItems.length) nextIndex = 0;
    setSelection(nextIndex);
  }

  function selectResult(item) {
    closeModal();
    // Scroll to the selected section
    const targetElement = document.querySelector(item.url);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth' });
      history.pushState(null, null, item.url);
    }
  }

  // Keyboard Trap inside search overlay
  modalOverlay.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      const focusable = modalOverlay.querySelectorAll('button, input, [tabindex="0"]');
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        last.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    }
  });
}

/* ==========================================================================
   COMPONENT 3: BUTTONS - VERSION SELECTOR DROPDOWN
   ========================================================================== */
function initVersionDropdown() {
  const trigger = document.getElementById('versionDropdownTrigger');
  const menu = document.getElementById('versionDropdownMenu');
  const currentVersionLabel = document.getElementById('currentVersionLabel');

  if (!trigger || !menu) return;

  function toggleDropdown() {
    const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
    trigger.setAttribute('aria-expanded', !isExpanded);
    menu.classList.toggle('active');
  }

  function closeDropdown() {
    trigger.setAttribute('aria-expanded', 'false');
    menu.classList.remove('active');
  }

  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDropdown();
  });

  // Select version and update UI label
  menu.querySelectorAll('.dropdown-link').forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Update selections
      menu.querySelectorAll('.dropdown-link').forEach(link => link.classList.remove('selected'));
      item.classList.add('selected');
      
      // Update label
      currentVersionLabel.textContent = item.dataset.version;
      closeDropdown();
      trigger.focus();
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!trigger.contains(e.target) && !menu.contains(e.target)) {
      closeDropdown();
    }
  });

  // Keyboard dropdown control
  trigger.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      toggleDropdown();
      const firstLink = menu.querySelector('.dropdown-link');
      if (firstLink) firstLink.focus();
    } else if (e.key === 'Escape') {
      closeDropdown();
    }
  });

  menu.addEventListener('keydown', (e) => {
    const links = Array.from(menu.querySelectorAll('.dropdown-link'));
    const currIndex = links.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      const nextLink = links[currIndex + 1] || links[0];
      if (nextLink) nextLink.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prevLink = links[currIndex - 1] || links[links.length - 1];
      if (prevLink) prevLink.focus();
    } else if (e.key === 'Escape') {
      closeDropdown();
      trigger.focus();
    }
  });
}

/* ==========================================================================
   COMPONENT 5: LISTS - COLLAPSIBLE DIRECTORY SECTIONS
   ========================================================================== */
function initCollapsibleDirectories() {
  const sections = document.querySelectorAll('.directory-section');

  sections.forEach(section => {
    const header = section.querySelector('.directory-header');
    
    if (!header) return;

    header.addEventListener('click', () => {
      const isCollapsed = section.classList.toggle('collapsed');
      header.setAttribute('aria-expanded', !isCollapsed);
    });

    header.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        section.classList.add('collapsed');
        header.setAttribute('aria-expanded', 'false');
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        section.classList.remove('collapsed');
        header.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/* ==========================================================================
   COMPONENT 3: BUTTONS - CODE COPY TO CLIPBOARD
   ========================================================================== */
function initCodeCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre');

  codeBlocks.forEach(block => {
    // Create button
    const btn = document.createElement('button');
    btn.className = 'btn btn-copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.innerHTML = `
      <svg class="copy-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
    `;
    
    block.appendChild(btn);

    btn.addEventListener('click', async () => {
      const codeElement = block.querySelector('code');
      if (!codeElement) return;

      const codeText = codeElement.innerText;
      
      try {
        await navigator.clipboard.writeText(codeText);
        
        // Show success state
        btn.innerHTML = `
          <svg class="check-icon" viewBox="0 0 24 24" width="16" height="16" stroke="#57cda4" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        `;
        btn.setAttribute('aria-label', 'Code copied');

        // Revert after 2 seconds
        setTimeout(() => {
          btn.innerHTML = `
            <svg class="copy-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          `;
          btn.setAttribute('aria-label', 'Copy code to clipboard');
        }, 2000);
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    });
  });
}

/* ==========================================================================
   ADVANCED RADIAL MASKRevealer / SPOTLIGHT PROXIMITY EFFECT
   ========================================================================== */
function initSpotlightEffect() {
  const cards = document.querySelectorAll('.spotlight-card');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      card.style.setProperty('--x', `${x}px`);
      card.style.setProperty('--y', `${y}px`);
    });
  });
}

/* ==========================================================================
   RESPONSIVE DESIGN Drawer Navigation & Backdrops
   ========================================================================== */
function initMobileNav() {
  const menuToggle = document.getElementById('menuToggleBtn');
  const sidebar = document.querySelector('.docs-sidebar');
  const body = document.body;
  
  if (!menuToggle || !sidebar) return;

  // Create backdrop
  const backdrop = document.createElement('div');
  backdrop.className = 'sidebar-backdrop';
  body.appendChild(backdrop);

  function toggleSidebar() {
    const isActive = sidebar.classList.toggle('active');
    backdrop.classList.toggle('active');
    menuToggle.setAttribute('aria-expanded', isActive);
  }

  function closeSidebar() {
    sidebar.classList.remove('active');
    backdrop.classList.remove('active');
    menuToggle.setAttribute('aria-expanded', 'false');
  }

  menuToggle.addEventListener('click', toggleSidebar);
  backdrop.addEventListener('click', closeSidebar);

  // Close sidebar drawer on link selection on mobile viewports
  sidebar.querySelectorAll('.directory-link, .sidebar-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 1024) closeSidebar();
    });
  });
}

/* ==========================================================================
   TABLE OF CONTENTS Scroll Spy Anchor Highlighting
   ========================================================================== */
function initTableOfContentsActiveState() {
  const sections = document.querySelectorAll('.js-anchor-section');
  const tocLinks = document.querySelectorAll('.toc-link');

  if (sections.length === 0 || tocLinks.length === 0) return;

  const observerOptions = {
    root: null,
    rootMargin: '-50px 0px -60% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        tocLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
            link.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach(section => observer.observe(section));
}
