import { NavLink } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SpeedIcon from '@mui/icons-material/Speed';
import StorageIcon from '@mui/icons-material/Storage';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutlineOutlined';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h2>API Intelligence</h2>
      </div>
      <ul className="nav-menu">
        <li>
          <NavLink to="/" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <DashboardIcon fontSize="small" /> Summary
          </NavLink>
        </li>
        <li>
          <NavLink to="/slow-apis" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <SpeedIcon fontSize="small" /> Slow APIs
          </NavLink>
        </li>
        <li>
          <NavLink to="/queries" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <StorageIcon fontSize="small" /> Slow Queries
          </NavLink>
        </li>
        <li>
          <NavLink to="/recommendations" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <LightbulbIcon fontSize="small" /> Recommendations
          </NavLink>
        </li>
        <li>
          <NavLink to="/issues" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
            <ErrorOutlineIcon fontSize="small" /> Issues
          </NavLink>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
