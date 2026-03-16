/**
 * A2CI Components Loader
 * Handles dynamic injection of shared UI elements (Header, Footer)
 */

document.addEventListener('DOMContentLoaded', () => {
  loadHeader();
  loadFooter();
});

async function loadHeader() {
  const headerContainer = document.getElementById('header-component');
  if (!headerContainer) return;

  try {
    const response = await fetch('components/header.html');
    const html = await response.text();
    headerContainer.innerHTML = html;
    initHeaderLogic();
    highlightActiveLink();
  } catch (error) {
    console.error('Error loading header:', error);
  }
}

async function loadFooter() {
  const footerContainer = document.getElementById('footer-component');
  if (!footerContainer) return;

  try {
    const response = await fetch('components/footer.html');
    const html = await response.text();
    footerContainer.innerHTML = html;
  } catch (error) {
    console.error('Error loading footer:', error);
  }
}

function initHeaderLogic() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  const iconMenu = document.getElementById('icon-menu');
  const iconClose = document.getElementById('icon-close');
  const mainHeader = document.getElementById('main-header');
  
  if (!btn || !menu) return;

  let isMenuOpen = false;

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
    if (isMenuOpen) {
      menu.classList.remove('max-h-0', 'opacity-0');
      menu.classList.add('max-h-[500px]', 'opacity-100', 'py-6');
      iconMenu.classList.add('opacity-0', '-rotate-90');
      iconClose.classList.remove('opacity-0', 'rotate-90');
    } else {
      closeMenu();
    }
  }

  function closeMenu() {
    isMenuOpen = false;
    menu.classList.remove('max-h-[500px]', 'opacity-100', 'py-6');
    menu.classList.add('max-h-0', 'opacity-0');
    iconMenu.classList.remove('opacity-0', '-rotate-90');
    iconClose.classList.add('opacity-0', 'rotate-90');
  }

  btn.addEventListener('click', toggleMenu);

  // Close menu on link click
  const navLinks = menu.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  // Header scroll effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      mainHeader.classList.add('header-scrolled');
    } else {
      mainHeader.classList.remove('header-scrolled');
    }
  });
}

function highlightActiveLink() {
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const links = document.querySelectorAll('.nav-link-agency, .nav-dropdown-trigger, .mobile-nav-link');
  
  links.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
      link.classList.add('text-[#E30613]', 'font-bold');
      const underline = link.querySelector('span');
      if (underline) underline.classList.replace('w-0', 'w-full');
    }
  });
}
