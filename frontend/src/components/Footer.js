import React from 'react';
import styled from 'styled-components';
import { HiOutlineChartPie, HiOutlineCode, HiOutlineHeart } from 'react-icons/hi';

const FooterContainer = styled.footer`
  background-color: var(--dark-bg);
  color: var(--light-text);
  padding: 3rem var(--content-padding) 2rem;
  margin-top: 4rem;
`;

const FooterContent = styled.div`
  max-width: var(--container-width);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  
  @media (min-width: 768px) {
    grid-template-columns: 1.5fr 1fr;
    align-items: start;
  }
`;

const FooterLogo = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  
  svg {
    font-size: 1.5rem;
    color: var(--secondary-color);
    margin-right: 0.75rem;
  }
  
  span {
    font-size: 1.25rem;
    font-weight: 600;
    background: linear-gradient(to right, #fff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
`;

const FooterText = styled.p`
  color: var(--text-tertiary);
  max-width: 400px;
  font-size: 0.875rem;
  line-height: 1.5;
`;

const LinkSection = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
`;

const LinkGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const LinkGroupTitle = styled.h4`
  color: white;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  font-weight: 600;
`;

const FooterLink = styled.a`
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    color: var(--secondary-color);
  }
`;

const Attribution = styled.div`
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 2rem;
  padding-top: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--text-tertiary);
  
  @media (max-width: 640px) {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
`;

const MadeWithLove = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  svg {
    color: var(--error-color);
  }
`;

function Footer() {
  return (
    <FooterContainer>
      <FooterContent>
        <div>
          <FooterLogo>
            <HiOutlineChartPie />
            <span>NutriCalc AI</span>
          </FooterLogo>
          
          <FooterText>
            Making nutrition science accessible for Indian cuisine. Our AI-powered
            calculator helps you understand the nutritional content of traditional
            dishes for healthier choices.
          </FooterText>
        </div>
        
        <LinkSection>
          <LinkGroup>
            <LinkGroupTitle>Resources</LinkGroupTitle>
            <FooterLink href="#">About AI Nutrition</FooterLink>
            <FooterLink href="#">Indian Food Database</FooterLink>
            <FooterLink href="#">Healthy Eating</FooterLink>
            <FooterLink href="#">Regional Dishes</FooterLink>
          </LinkGroup>
          
          <LinkGroup>
            <LinkGroupTitle>Company</LinkGroupTitle>
            <FooterLink href="#">About Us</FooterLink>
            <FooterLink href="#">Privacy Policy</FooterLink>
            <FooterLink href="#">Terms of Use</FooterLink>
            <FooterLink href="#">
              <HiOutlineCode size={14} />
              GitHub
            </FooterLink>
          </LinkGroup>
        </LinkSection>
      </FooterContent>
      
      <Attribution>
        <div>© {new Date().getFullYear()} NutriCalc AI • Nutrition data from IFCT-2017</div>
        <MadeWithLove>
          <span>Made with</span>
          <HiOutlineHeart />
          <span>in India</span>
        </MadeWithLove>
      </Attribution>
    </FooterContainer>
  );
}

export default Footer;
