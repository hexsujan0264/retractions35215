import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load the dataset
file_path = 'retractions35215.csv'
retractions_df = pd.read_csv(file_path)

# Handle missing values
retractions_df['Institution'].fillna('Unknown', inplace=True)
retractions_df['RetractionDOI'].fillna('Unknown', inplace=True)
retractions_df['OriginalPaperPubMedID'].fillna(0, inplace=True)
retractions_df['Paywalled'].fillna('Unknown', inplace=True)

# Convert date fields to appropriate datetime formats
retractions_df['RetractionDate'] = pd.to_datetime(retractions_df['RetractionDate'], format='%m/%d/%Y', errors='coerce')
retractions_df['OriginalPaperDate'] = pd.to_datetime(retractions_df['OriginalPaperDate'], format='%m/%d/%Y', errors='coerce')

# Handle any potential missing dates by dropping rows with NaT values in date columns
retractions_df.dropna(subset=['RetractionDate', 'OriginalPaperDate'], inplace=True)

# Normalize categorical fields
categorical_fields = ['Subject', 'Institution', 'Journal', 'Publisher', 'Country', 'Author', 'ArticleType', 'RetractionNature', 'Reason', 'Paywalled']
for field in categorical_fields:
    retractions_df[field] = retractions_df[field].str.lower()

# Add year columns for analysis
retractions_df['RetractionYear'] = retractions_df['RetractionDate'].dt.year
retractions_df['OriginalPaperYear'] = retractions_df['OriginalPaperDate'].dt.year

# Plot the number of retractions per year
yearly_retractions = retractions_df['RetractionYear'].value_counts().sort_index()

plt.figure(figsize=(14, 7))
sns.lineplot(x=yearly_retractions.index, y=yearly_retractions.values, marker='o')
plt.title('Number of Retractions per Year')
plt.xlabel('Year')
plt.ylabel('Number of Retractions')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot the number of original papers published per year for retracted papers
original_papers_per_year = retractions_df['OriginalPaperYear'].value_counts().sort_index()

plt.figure(figsize=(14, 7))
sns.lineplot(x=original_papers_per_year.index, y=original_papers_per_year.values, marker='o')
plt.title('Number of Original Papers Published per Year for Retracted Papers')
plt.xlabel('Year')
plt.ylabel('Number of Original Papers')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot common reasons for retraction
reasons = retractions_df['Reason'].str.split(';', expand=True).stack().value_counts().head(10)

plt.figure(figsize=(14, 7))
sns.barplot(x=reasons.values, y=reasons.index)
plt.title('Top 10 Common Reasons for Retraction')
plt.xlabel('Count')
plt.ylabel('Reason')
plt.tight_layout()
plt.show()

# Plot trends by subject
subject_retractions = retractions_df['Subject'].value_counts().head(10)

plt.figure(figsize=(14, 7))
sns.barplot(x=subject_retractions.values, y=subject_retractions.index)
plt.title('Top 10 Subjects by Number of Retractions')
plt.xlabel('Count')
plt.ylabel('Subject')
plt.tight_layout()
plt.show()

# Plot trends by institution
institution_retractions = retractions_df['Institution'].value_counts().head(10)

plt.figure(figsize=(14, 7))
sns.barplot(x=institution_retractions.values, y=institution_retractions.index)
plt.title('Top 10 Institutions by Number of Retractions')
plt.xlabel('Count')
plt.ylabel('Institution')
plt.tight_layout()
plt.show()

# Plot trends by journal
journal_retractions = retractions_df['Journal'].value_counts().head(10)

plt.figure(figsize=(14, 7))
sns.barplot(x=journal_retractions.values, y=journal_retractions.index)
plt.title('Top 10 Journals by Number of Retractions')
plt.xlabel('Count')
plt.ylabel('Journal')
plt.tight_layout()
plt.show()

# Plot trends by country
country_retractions = retractions_df['Country'].str.split(';', expand=True).stack().value_counts().head(10)

plt.figure(figsize=(14, 7))
sns.barplot(x=country_retractions.values, y=country_retractions.index)
plt.title('Top 10 Countries by Number of Retractions')
plt.xlabel('Count')
plt.ylabel('Country')
plt.tight_layout()
plt.show()


# Additional Analysis: Retraction Reasons Over Time
# Group by year and reason
retractions_df['Reason'] = retractions_df['Reason'].str.split(';')
reasons_over_time = retractions_df.explode('Reason')
reasons_over_time = reasons_over_time.groupby(['RetractionYear', 'Reason']).size().unstack().fillna(0)



# Additional Analysis: Retraction by Article Type
article_type_retractions = retractions_df['ArticleType'].value_counts().head(10)

plt.figure(figsize=(14, 7))
sns.barplot(x=article_type_retractions.values, y=article_type_retractions.index)
plt.title('Top 10 Article Types by Number of Retractions')
plt.xlabel('Count')
plt.ylabel('Article Type')
plt.tight_layout()
plt.show()
