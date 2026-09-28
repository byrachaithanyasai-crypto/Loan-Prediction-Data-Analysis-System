import React, { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { getHealth } from '../services/api';

export default function Layout() {
  const [isOnline, setIsOnline] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    getHealth().then(() => setIsOnline(true)).catch(() => setIsOnline(false));
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-brand-light font-sans text-brand-dark">
      <Sidebar isOpen={mobileMenuOpen} closeMenu={() => setMobileMenuOpen(false)} />
      <div className="flex-1 md:ml-64 flex flex-col h-full overflow-hidden w-full">
        <Navbar isOnline={isOnline} toggleMenu={() => setMobileMenuOpen(!mobileMenuOpen)} />
        <main className="flex-1 overflow-y-auto p-4 md:p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
