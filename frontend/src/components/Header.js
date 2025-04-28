import React from 'react';
import styled from 'styled-components';
import { HiOutlineSparkles, HiOutlineChartPie } from 'react-icons/hi';

const HeaderContainer = styled.header`
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  padding: 1.5rem var(--content-padding);
  position: relative;
  overflow: hidden;
`;

const HeaderContent = styled.div`
  max-width: var(--container-width);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;

  svg {
    font-size: 1.75rem;
    color: rgba(255, 255, 255, 0.9);
  }

  h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: white;
    margin: 0;
    letter-spacing: -0.02em;
  }

  @media (max-width: 640px) {
    h1 {
      font-size: 1.5rem;
    }

    svg {
      font-size: 1.5rem;
    }
  }
`;

const Subtitle = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
  font-weight: 500;
`;

const Version = styled.span`
  background: rgba(255, 255, 255, 0.15);
  padding: 0.15rem 0.5rem;
  border-radius: var(--border-radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.5rem;
`;

const BackgroundPattern = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: radial-gradient(circle at 25% 100%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
  z-index: 1;
`;

const SparkleIcon = styled(HiOutlineSparkles)`
  position: absolute;
  color: rgba(255, 255, 255, 0.15);
  &.small {
    font-size: 1rem;
    top: 25%;
    right: 20%;
    animation: pulse 3s infinite ease-in-out;
  }
  &.medium {
    font-size: 1.5rem;
    top: 40%;
    left: 25%;
    animation: pulse 4s infinite ease-in-out;
  }
  &.large {
    font-size: 2rem;
    bottom: 20%;
    right: 35%;
    animation: pulse 5s infinite ease-in-out;
  }
`;

function Header() {
  return (
    <HeaderContainer>
      <BackgroundPattern />
      <SparkleIcon className="small" />
      <SparkleIcon className="medium" />
      <SparkleIcon className="large" />
      
      <HeaderContent>
        <Logo>
          <HiOutlineChartPie />
          <h1>NutriCalc AI</h1>
        </Logo>
        <Subtitle>
          Nutritional intelligence for Indian cuisine
          <Version>v2.1</Version>
        </Subtitle>
      </HeaderContent>
    </HeaderContainer>
  );
}

export default Header;
