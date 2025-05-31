FROM node:18
WORKDIR /app
COPY ui/package.json ./ 
RUN npm install
COPY ui/ ./  
CMD ["npm", "start"]